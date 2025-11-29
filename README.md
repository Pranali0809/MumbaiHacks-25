# **Vaidya AI — Agentic Healthcare Assistant**  
### *Built for MumbaiHacks25*

Project Demo: [Watch our Demo recording]([https://1drv.ms/v/c/0bc632da0eda4e46/IQB6O7-JVsurRIw4BWVJgp35AXUajwA08rbWJQze6D9nILM?e=2R9UAc])

Vaidya AI is an AI-powered, agentic healthcare application designed to streamline the doctor–patient journey. By automating pre-consultation questioning, generating clinical summaries, and assisting doctors with decision support, Vaidya AI reduces administrative workload and enhances patient experience.

Below is a polished, professional, and compelling **README.md** for your multi-agent medical diagnostics project.
It is structured, impressive, technically sound, and easy for judges, developers, and reviewers to understand.

---

# # 🏥 **Vaidya — Multi-Agent Medical Diagnostic System**

### *AI-powered clinical reasoning with autonomous agents, structured patient data, and human-verified diagnosis.*

---

## 🚀 **Overview**

**Vaidya** is a next-generation **multi-agent medical diagnostic platform** designed to eliminate fragmented patient data and assist doctors with intelligent, structured clinical insights.
Built using **Google ADK**, **Agent Engine**, **RAC pipelines**, **vector search**, and **medical LLMs (MedBolt / BioGPT)**, the system automates the **SOAP** process end-to-end:

* **S — Subjective** (Patient history intake)
* **O — Objective** (Doctor notes + labs + reports)
* **A — Assessment** (AI-driven diagnosis)
* **P — Plan** (Doctor-verified treatment plan)

This enables faster, safer, and more accurate clinical decision-making — with doctors always in control as the final authority.

---

## 🧩 **System Architecture**

Vaidya uses a **multi-agent workflow**, each agent specializing in one part of the diagnostic process.

### **1. Pre-Appointment: Subjective Agent (S-Agent)**

**Purpose:** Collects patient history using structured questioning.

**Flow:**

* Patient initiates Pre-Assessment.
* S-Agent (built using **ADK + Agent Engine** with MedBolt/BioGPT) collects HPI.
* Outputs:

  * Subjective transcript
  * Structured JSON medical summary
* Stored in Firestore under `appointments.pre_assessment`.

---

### **2. Objective Data Integration**

**Purpose:** Consolidate real-world medical data from multiple sources.

**Inputs:**

* Doctor’s audio → transcribed via **Whisper + MCP pipeline**
* Lab test results
* Diagnostic reports
* Imaging summaries

Everything is organized and accessible via the patient dashboard.

---

### **3. AI Diagnosis Agent (Assessment)**

**Purpose:** Generate clinically aligned assessments and differentials.

**Inputs:**

* Full patient history (EHR)
* S-Agent summary
* Doctor–patient transcript

**Processing Pipeline:**

* RAC (Retrieval-Augmented Conversation)
* FAISS/Chroma vector DB
* Medical knowledge graph
* MedBolt/BioGPT for reasoning
* MCP for structured tool access

**Outputs:**

* Possible diagnoses (ranked)
* Recommended prescriptions
* Suggested labs/tests
* Auto-generated consultation notes

---

### **4. Doctor Review & Care Plan (PLAN)**

**Human-in-the-loop validation.**
Doctor reviews all generated suggestions and selects:

* Final diagnoses
* Prescriptions
* Labs/tests
* Visit notes

System then:

* Converts appointment → doctor visit
* Updates patient’s medical timeline
* Adds items to dashboard under **Plan**

---

## 🗂️ **Folder Structure**

```
├── agents/
│   ├── subjective_agent/
│   ├── diagnosis_agent/
│   └── objective_pipeline/
├── api/
│   ├── firebase/
│   ├── whisper_mcp/
│   └── vector_search/
├── frontend/
│   └── patient_dashboard/
├── backend/
│   └── appointment_service/
├── models/
│   └── medbolt_biogpt/
├── README.md
```

---

## 🧠 **Tech Stack**

### **AI & Multi-Agent Framework**

* Google **ADK (Agent Developer Kit)**
* Vertex AI **Agent Engine**
* RAC (Retrieval-Augmented Conversation)
* MCP (Model Context Protocol)
* BioGPT / MedBolt for clinical reasoning
* Whisper for audio transcription

### **Backend**

* Node.js / Python microservices
* Firestore for EHR & timeline storage
* FAISS / Chroma for vector search

### **Frontend**

* React / Next.js dashboard for doctors & patients

### **Pipelines**

* Audio → Whisper → MCP
* Labs → OCR / structured parser
* EHR → RAC pipeline for diagnosis agent

---

## 🔥 **Key Features**

* Full **SOAP-mapped multi-agent workflow**
* Autonomous **Subjective intake agent**
* Automatic integration of **objective clinical data**
* AI-powered **diagnosis generation**
* **Human-in-the-loop** doctor verification
* Real-time synchronization with EHR & visit timeline
* Modular agents deployable individually or as a pipeline

---

## 🏆 **Why Vaidya Stands Out**

* Built for **real clinical workflows**
* Designed with **doctor-centric** control
* Moves beyond chatbots → a **true autonomous agentic system**
* Reduces diagnostic gaps through **cross-data correlation**
* Achieves structured medical reasoning at scale

---

## 🧪 **How to Run (Development Setup)**

### **1. Install dependencies**

```bash
pip install -r requirements.txt
npm install
```

### **2. Configure Environment**

* Add Firebase credentials
* Add Whisper + MCP API keys
* Add Google ADK + Vertex AI configs

### **3. Start Agents**

```bash
python agents/subjective_agent/main.py
python agents/diagnosis_agent/main.py
```

### **4. Start Backend**

```bash
npm run start
```

### **5. Start Frontend**

```bash
npm run dev
```

---

## 💡 **Future Enhancements**

* Symptom progression graphing
* Real-time vitals ingestion (IoT)
* Drug–drug interaction warning system
* Multi-language patient intake
* Integration with government health exchanges

---

## 🤝 **Team**

**Vaidya.ai by Mavericks**
Passionate engineers building the future of medical AI.

---

If you want, I can also generate:

✅ A shorter **developer-friendly README**
✅ A pitch-friendly **executive summary README**
✅ A visual diagram (Mermaid) to embed in the README

Just tell me!

---

