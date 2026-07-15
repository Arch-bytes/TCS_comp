from models import CandidateProfile, InterviewResponse


CANDIDATES = [
    {
        "profile": CandidateProfile(
            candidate_id="CAN-001",
            name="Aisha Rahman",
            claimed_skills=["Python", "FastAPI", "PostgreSQL"],
            resume_text=(
                "Experience building high-performance APIs using Python and FastAPI. "
                "Designed scalable databases and query optimization with PostgreSQL."
            ),
        ),
        "response": InterviewResponse(
            candidate_id="CAN-001",
            question="Can you describe how you optimize database performance in a python backend?",
            expected_skill="Python",
            answer_text=(
                "I use Python and FastAPI to build RESTful services. In my last project, I integrated "
                "a PostgreSQL database and optimized query latency by adding indexing on frequently read "
                "columns and implementing connection pooling, which improved response times by 30%."
            ),
            observation_flags=[],
        ),
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-002",
            name="Liam Vance",
            claimed_skills=["Kubernetes", "Docker", "AWS"],
            resume_text=(
                "DevOps engineer specializing in container orchestration with Kubernetes, Docker, and cloud deployments on AWS."
            ),
        ),
        "response": InterviewResponse(
            candidate_id="CAN-002",
            question="How do you handle container scaling and pod recovery in a production Kubernetes cluster?",
            expected_skill="Kubernetes",
            answer_text=(
                "Yes, I know about computers and cloud. I can run basic commands and configure simple settings "
                "on a local machine, but I have not had a chance to work with container orchestration or cluster setup directly."
            ),
            observation_flags=[],
        ),
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-003",
            name="Sarah Jenkins",
            claimed_skills=["React", "TypeScript", "TailwindCSS"],
            resume_text=(
                "Frontend developer building responsive user interfaces using React, TypeScript, and TailwindCSS."
            ),
        ),
        "response": InterviewResponse(
            candidate_id="CAN-003",
            question="What are the benefits of using TypeScript with React components?",
            expected_skill="React",
            answer_text=(
                "React is a component-based frontend library. I use TypeScript for type safety and TailwindCSS for clean, rapid layout designs. "
                "In my previous role, I migrated our legacy landing page to React components and enforced strict typing for props."
            ),
            observation_flags=["unnatural_blink"],
        ),
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-004",
            name="Mina Sol",
            claimed_skills=["Machine Learning", "PyTorch", "NLP"],
            resume_text=(
                "ML engineer with a focus on training deep learning models in PyTorch and deploying NLP transformers."
            ),
        ),
        "response": InterviewResponse(
            candidate_id="CAN-004",
            question="Explain how you use PyTorch to train an LSTM model.",
            expected_skill="PyTorch",
            answer_text=(
                "As an AI language model, I do not have personal experience, but I can state that PyTorch is an open-source machine learning library. "
                "In conclusion, PyTorch offers dynamic computational graphs which make it easy to build LSTMs."
            ),
            observation_flags=[],
        ),
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-005",
            name="Noah Kim",
            claimed_skills=["Go", "gRPC", "Redis"],
            resume_text=(
                "Backend engineer building microservices in Go, using gRPC for inter-service communication and Redis for caching."
            ),
        ),
        "response": InterviewResponse(
            candidate_id="CAN-005",
            question="Why choose gRPC over REST for microservices?",
            expected_skill="Go",
            answer_text=(
                "We write microservices in Go because of its concurrency model and speed. We use gRPC to transmit protobuf payloads efficiently and Redis for caching session data."
            ),
            observation_flags=["lip_sync_error", "audio_unsynced"],
        ),
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-006",
            name="Elena Rostova",
            claimed_skills=["Cybersecurity", "Penetration Testing", "Wireshark"],
            resume_text=(
                "Security analyst with hands-on experience in penetration testing, network monitoring using Wireshark, and threat analysis."
            ),
        ),
        "response": InterviewResponse(
            candidate_id="CAN-006",
            question="How do you filter packet captures in Wireshark to locate suspicious DNS queries?",
            expected_skill="Wireshark",
            answer_text=(
                "As an AI, I cannot perform penetration testing. However, Wireshark is used to capture network packets. "
                "My knowledge cutoff is January 2025, so I can only speak to standard packet inspection techniques."
            ),
            observation_flags=["multiple_voices", "background_swapped"],
        ),
    },
    {
        "profile": CandidateProfile(
            candidate_id="CAN-007",
            name="Jordan Smith",
            claimed_skills=["Python", "Machine Learning", "Data Science"],
            resume_text=(
                "Expert in Python programming and Machine Learning model training. "
                "Skilled in deep learning, neural networks, and advanced data science pipelines."
            ),
        ),
        "response": InterviewResponse(
            candidate_id="CAN-007",
            question="Explain basic Python lists and the steps you take to train a machine learning model.",
            expected_skill="Python",
            answer_text=(
                "I have used computers for a long time and I am very familiar with technology. "
                "I can install software and navigate different operating systems easily. "
                "I am a hard worker and I learn new tools very quickly whenever I am given a task."
            ),
            observation_flags=["prompting_detected", "poor_eye_contact"],
        ),
    },
]
