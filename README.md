# 🩺 CareSync — AI-Powered Recovery & Nutrition Assistant

CareSync is an intelligent, end-to-end healthcare assistant that predicts recovery time, recommends personalized diet plans, and generates structured health reports using Generative AI.

The system combines **Machine Learning + Conversational UI + Generative AI** to deliver a seamless, user-friendly healthcare guidance experience.

---

## 🚀 Key Features

### 🔹 Recovery Time Prediction
- Machine Learning regression model
- Estimates recovery duration based on health and lifestyle inputs

### 🔹 Personalized Diet Recommendation
- Classification-based model
- Considers BMI, condition type, and activity levels

### 🔹 AI-Generated Health Reports
- Powered by OpenAI (Generative AI)
- Converts predictions into clear, human-readable insights
- Includes recommendations and disclaimers

### 🔹 Conversational Interface
- Chat-based interaction instead of traditional forms
- Improves usability and engagement

### 🔹 Shareable Reports
- Reports stored in database
- Unique shareable links generated for each user

### 🔹 Observability & Monitoring
- Prometheus metrics integration
- Grafana dashboards for performance tracking

---

## 🏗️ Tech Stack

| Layer            | Technology |
|------------------|-----------|
| Frontend         | HTML, CSS, JavaScript (Tailwind CSS) |
| Backend          | FastAPI (Python) |
| Machine Learning | Scikit-learn |
| Generative AI    | OpenAI API |
| Database         | NeonDB (PostgreSQL) |
| Monitoring       | Prometheus, Grafana |
| Deployment       | Vercel |
| Containerization | Docker |

---
## 📊 System Architecture

<img width="1536" height="1024" alt="CareSyncArchitecture" src="https://github.com/user-attachments/assets/40746377-9fec-41d7-82ce-b54c2933ad74" />

---

---

## ⚙️ Core System Workflow

1. User interacts via conversational UI  
2. Inputs are validated and processed  
3. Feature engineering applied (e.g., BMI calculation)  
4. ML models generate predictions:
   - Recovery time  
   - Diet recommendation  
5. OpenAI generates a structured health report  
6. Results stored in NeonDB  
7. Shareable report link generated  
8. Metrics exposed for monitoring  

---

## 📈 Observability

CareSync integrates monitoring to ensure reliability and performance.

### Metrics Tracked
- API response time  
- Request throughput  
- Error rate  
- Endpoint usage  

### Monitoring Stack
- **Prometheus** → Collects metrics via `/metrics` endpoint  
- **Grafana** → Visualizes performance dashboards  

---

## 🔐 Security

- Input validation for all user data  
- Secure handling of API keys using environment variables  
- Encrypted database connections (SSL via NeonDB)  
- Backend API isolation  

---

## 🧪 Testing Strategy

- UI testing for conversational flow  
- API testing for endpoints  
- Input validation testing (edge cases)  
- Model output verification  
- End-to-end workflow validation  

---

## 🚀 Deployment

- Frontend hosted on **Vercel**  
- Backend served via **FastAPI**  
- Database managed using **NeonDB**  
- Containerized backend using **Docker**  

---

## ⚠️ Limitations

- Not a substitute for professional medical advice  
- Limited dataset for training models  
- Basic ML models (can be further optimized)  
- No real-time integration with healthcare systems  

---

## 🔮 Future Enhancements

- User authentication and profiles  
- Integration with real-world healthcare datasets  
- Advanced ML / Deep Learning models  
- Wearable device (IoT) integration  
- Real-time alerts and notifications  
- Expanded condition coverage  

---

## 📂 Repository Structure
<img width="243" height="582" alt="image" src="https://github.com/user-attachments/assets/7a50bc4c-fff7-48ca-b894-ae4066723895" />

---

## 📌 GitHub Evaluation Notes

- Clean and modular architecture  
- Fully reproducible structure  
- Clear separation of frontend, backend, and ML components  
- Version-controlled development with meaningful commits  
- Well-documented repository  

---

## 📜 Disclaimer

CareSync is intended for **educational and informational purposes only**.  
It does **not** provide medical advice. Always consult a qualified healthcare professional for medical decisions.

---
