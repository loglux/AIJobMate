from crewai import Crew, Agent, Task
from profile_manager import ProfileManager

profile_manager = ProfileManager("data/profile.json")

def run_career_crew(job_description: str, model_cv: str, model_cover: str, model_qa: str):
    profile = profile_manager.load()

    cv_agent = Agent(
        role="CV Writer",
        goal="Generate a UK-style CV for the provided job",
        backstory="An expert in crafting concise, targeted CVs that highlight strengths and relevant experience.",
        verbose=True,
        llm=f"ollama/{model_cv}"
    )

    cover_letter_agent = Agent(
        role="Cover Letter Specialist",
        goal="Write a persuasive and tailored UK-style cover letter",
        backstory="Experienced HR writer specialising in job-specific motivation letters.",
        verbose=True,
        llm=f"ollama/{model_cover}"
    )

    qa_agent = Agent(
        role="Quality Assurance Reviewer",
        goal="Review and refine CV and cover letter content",
        backstory="A meticulous proofreader who checks documents for clarity, tone, and alignment with the job post.",
        verbose=True,
        llm=f"ollama/{model_qa}"
    )

    cv_task = Task(
        description=f"Generate a UK-style CV for this job: {job_description}\n\nProfile: {profile}",
        expected_output="Concise, relevant CV content",
        agent=cv_agent
    )

    cover_task = Task(
        description=f"Write a UK-style cover letter for this role: {job_description}\n\nCandidate profile: {profile}",
        expected_output="Polished cover letter with job match justification",
        agent=cover_letter_agent
    )

    review_task = Task(
        description="Review the generated CV and cover letter for errors, clarity, and completeness.",
        expected_output="Final version of CV and cover letter with corrections",
        agent=qa_agent
    )

    crew = Crew(
        agents=[cv_agent, cover_letter_agent, qa_agent],
        tasks=[cv_task, cover_task, review_task],
        verbose=True
    )

    crew.kickoff()

    return {
        "cv": str(cv_task.output),
        "cover_letter": str(cover_task.output),
        "review": str(review_task.output)
    }
