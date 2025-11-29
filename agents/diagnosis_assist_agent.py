from vertexai import agent_engines
import vertexai
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from pydantic import BaseModel, Field
from typing import List, Optional

vertexai.init(
    project="stellar-chariot-477813-u9",
    location="us-central1",
    api_endpoint="us-central1-aiplatform.googleapis.com"
)

rag_corpus = "projects/stellar-chariot-477813-u9/locations/us-east1/ragCorpora/2305843009213693952"

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_rag_documentation',
    description=(
        'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
    ),
    rag_resources=[
        rag.RagResource(rag_corpus)
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)


class DiagnosisOption(BaseModel):
    name: str
    selected: bool = False


class PrescriptionOption(BaseModel):
    name: str
    dosage: Optional[str] = None
    selected: bool = False


class TestOption(BaseModel):
    name: str
    selected: bool = False


class ActionItem(BaseModel):
    text: str


class DiagnosisOutput(BaseModel):
    possible_diagnoses: List[DiagnosisOption] = Field(default_factory=list)
    suggested_prescriptions: List[PrescriptionOption] = Field(
        default_factory=list)
    recommended_tests: List[TestOption] = Field(default_factory=list)
    doctor_action_items: List[ActionItem] = Field(default_factory=list)


GEMINI_MODEL = "gemini-2.5-pro"

clinical_analyzer_agent = Agent(
    name="ClinicalAnalyzerAgent",
    model=GEMINI_MODEL,
    instruction="""
You are a focused clinical extraction agent.
Input: raw patient conversation / history text (state['patient_text']).

Task:
- Extract structured clinical facts and output JSON ONLY (no commentary).
- JSON schema:
{
  "symptoms": ["..."],
  "duration": "text or empty",
  "history": ["..."],
  "red_flags": ["..."],
  "vitals": {"bp":"", "hr":"", "temp":""} or {},
  "other_notes": "free text"
}
If a field is not present, return empty list / empty string / empty object as appropriate.
""",
    description="Extract structured clinical facts from unstructured text.",
    output_key="extracted_data",
)


medical_retrieval_agent = Agent(
    name="MedicalRetrievalAgent",
    model=GEMINI_MODEL,
    instruction="""
You are a query builder and retrieval orchestrator.
Input: state['extracted_data'] (JSON produced by ClinicalAnalyzerAgent).

Task:
1) Construct a concise, high-signal retrieval query using the extracted fields (symptoms, duration, history, red_flags).
2) Output the single-line query string ONLY (no JSON, no extra commentary).
""",
    description="Creates a compact RAG query from extracted clinical facts.",
    output_key="rag_query",
)

rag_execution_agent = Agent(
    name="RAGExecutionAgent",
    model=GEMINI_MODEL,
    instruction="""
This stage executes the retrieval query against the RAG corpus.
Input: state['rag_query'] (string).

Action required by runtime: call your local rag retrieval function with this query:
    retrieved_text = ask_vertex_retrieval(rag_query)

Then return retrieved_text (plain text). If there are no results, return an empty string.
Do not add commentary—output only the retrieved text or an empty string.
""",
    description="Executes RAG retrieval for the provided query.",
    tools=[
        ask_vertex_retrieval
    ],
    output_key="rag_results",
)


# -------------------------
# Synthesizer Agent (now explicitly directed to match the DiagnosisOutput schema)
# -------------------------
clinical_synthesizer_agent = Agent(
    name="ClinicalSynthesizerAgent",
    model=GEMINI_MODEL,
    instruction="""
You are an advanced clinical reasoning and synthesis agent.

You receive:
- state['extracted_data'] → structured symptoms & history
- state['rag_results'] → retrieved evidence text (may be empty)

Your job: Produce a **high-detail but schema-aligned output**.

-------------------------
### **IF RAG evidence is available and relevant**
- Use it explicitly during reasoning.
- Incorporate evidence-supported findings.
- Make the differentials more detailed (pathophysiology & key discriminators).
- Ensure recommendations reflect what evidence suggests.

### **IF RAG evidence is empty or irrelevant**
- Fall back to your own clinical expertise.
- Still produce high-detail output.

-------------------------
### **OUTPUT REQUIREMENTS (STRICT)**

You must output **VALID JSON ONLY** following *exactly* the schema below:

{
  "possible_diagnoses": [
    {"name": "", "selected": false}
  ],
  "suggested_prescriptions": [
    {"name": "", "dosage": "", "selected": false}
  ],
  "recommended_tests": [
    {"name": "", "selected": false}
  ],
  "doctor_action_items": [
    {"text": ""}
  ]
}

-------------------------
### **CONTENT RULES**

1. **possible_diagnoses**  
   - Provide 4–6 highly detailed differential diagnoses.  
   - Each diagnosis MUST include:
     - clear diagnostic label  
     - precise clinical reasoning (added in parentheses after the name)  
     - pathophysiologic explanation  
     - key distinguishing features  

   Example formatting:  
   `"name": "Hyperthyroidism (thyroid hormone excess leading to sympathetic overactivity and weight loss)"`

2. **suggested_prescriptions**
   - Provide 3–5 medications with:
     - exact dosage  
     - standard frequency  
     - indication reasoning (in parentheses after name)  
   - Choose prescriptions appropriate to the clinical scenario.

3. **recommended_tests**
   - Provide 3–6 diagnostic tests
   - Each must include clear clinical justification (included after the name in parentheses)
   - Ensure tests follow evidence-based clinical pathways.

4. **doctor_action_items**
   - Provide 3–5 actionable clinician follow-up items.
   - Items should include monitoring instructions, safety-net advice, or clinical priorities.

-------------------------
### **ADDITIONAL RULES**
- No text outside the JSON.
- No comments.
- No ellipses (“...”).
- Do NOT include “explanation” field anymore.
- Keep all “selected” values defaulted to false.
""",
    description="Synthesize final structured diagnosis output matching the Pydantic schema.",
    output_key="final_report",
    output_schema=DiagnosisOutput,
)

# -------------------------
# Sequential Agent Chain (Main Workflow)
# -------------------------

root_agent = SequentialAgent(
    agents=[
        clinical_analyzer_agent,
        medical_retrieval_agent,
        rag_execution_agent,
        clinical_synthesizer_agent,
    ]
)

# Wrap the agent in an AdkApp object
med_app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)
