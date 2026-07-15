from models import CandidateProfile, InterviewResponse

# A set of mock candidate profiles and their corresponding interview responses.
CANDIDATES = [
    {
        "profile": CandidateProfile(
            candidate_id="CAN-001",
            name="Aisha Rahman",
            claimed_skills=["Python", "FastAPI", "PostgreSQL"],
            resume_text="Experience building high-performance APIs using Python and FastAPI. Designed scalable databases and query optimization with PostgreSQL."
        ),
        "response": InterviewResponse(
            candidate_id="CAN-001",
            question="Can you describe how you optimize database performance in a python backend?",
            expected_skill="Python",
            answer_text="I use Python and FastAPI to build RESTful services. In my last project, I integrated a PostgreSQL database and optimized query latency by adding indexing on frequently read columns and implementing connection pooling, which improved response times by 30%.",
            observation_flags=[]
        ),
        "description": "Low Risk (Genuine candidate with good skill matching and clean video feed)"
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-002",
            name="Liam Vance",
            claimed_skills=["Kubernetes", "Docker", "AWS"],
            resume_text="DevOps Engineer specializing in container orchestration with Kubernetes, Docker, and cloud deployments on AWS."
        ),
        "response": InterviewResponse(
            candidate_id="CAN-002",
            question="How do you handle container scaling and pod recovery in a production Kubernetes cluster?",
            expected_skill="Kubernetes",
            answer_text="Yes, I know about computers and cloud. I can run basic commands and configure simple settings on a local machine, but I have not had a chance to work with container orchestration or cluster setup directly.",
            observation_flags=[]
        ),
        "description": "Medium Risk (Low similarity match between answer and resume claimed skills)"
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-003",
            name="Sarah Jenkins",
            claimed_skills=["React", "TypeScript", "TailwindCSS"],
            resume_text="Frontend developer building responsive user interfaces using React, TypeScript, and TailwindCSS."
        ),
        "response": InterviewResponse(
            candidate_id="CAN-003",
            question="What are the benefits of using TypeScript with React components?",
            expected_skill="React",
            answer_text="React is a component-based frontend library. I use TypeScript for type safety and TailwindCSS for clean, rapid layout designs. In my previous role, I migrated our legacy landing page to React components and enforced strict typing for props.",
            observation_flags=["unnatural_blink"]
        ),
        "description": "Medium Risk (Good skill match but triggered a minor observation flag: 'unnatural_blink')"
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-004",
            name="Michael Scott",
            claimed_skills=["Machine Learning", "PyTorch", "NLP"],
            resume_text="ML Engineer with a focus on training deep learning models in PyTorch and deploying NLP transformers."
        ),
        "response": InterviewResponse(
            candidate_id="CAN-004",
            question="Explain how you use PyTorch to train an LSTM model.",
            expected_skill="PyTorch",
            answer_text="As an AI language model, I do not have personal experience, but I can state that PyTorch is an open-source machine learning library. In conclusion, PyTorch offers dynamic computational graphs which make it easy to build LSTMs.",
            observation_flags=[]
        ),
        "description": "High Risk (Canned/Robotic AI assistant phrases detected in the answer text)"
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-005",
            name="David Kim",
            claimed_skills=["Go", "gRPC", "Redis"],
            resume_text="Backend engineer building microservices in Go, using gRPC for inter-service communication and Redis for caching."
        ),
        "response": InterviewResponse(
            candidate_id="CAN-005",
            question="Why choose gRPC over REST for microservices?",
            expected_skill="Go",
            answer_text="We write microservices in Go because of its concurrency model and speed. We use gRPC to transmit protobuf payloads efficiently and Redis for caching session data.",
            observation_flags=["lip_sync_error", "audio_unsynced"]
        ),
        "description": "High Risk (Critical deepfake observation signatures: lip-sync error and unsynced audio)"
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-006",
            name="Elena Rostova",
            claimed_skills=["Cybersecurity", "Penetration Testing", "Wireshark"],
            resume_text="Security analyst with hands-on experience in penetration testing, network monitoring using Wireshark, and threat analysis."
        ),
        "response": InterviewResponse(
            candidate_id="CAN-006",
            question="How do you filter packet captures in Wireshark to locate suspicious DNS queries?",
            expected_skill="Wireshark",
            answer_text="As an AI, I cannot perform penetration testing. However, Wireshark is used to capture network packets. My knowledge cutoff is January 2025, so I can only speak to standard packet inspection techniques.",
            observation_flags=["multiple_voices", "background_swapped"]
        ),
        "description": "High Risk (Combination of robotic response phrases and multiple critical/warning video-audio observation flags)"
    }
]
