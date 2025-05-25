import gradio as gr
from profile_manager import ProfileManager
from llm_engines.ollama_client import OllamaClient
from career_crew import run_career_crew

profile_manager = ProfileManager("data/profile.json")

def get_available_models():
    client = OllamaClient()
    return client.list_models()

def generate_docs(job_description, model_cv, model_cover, model_qa):
    output = run_career_crew(
        job_description=job_description,
        model_cv=model_cv,
        model_cover=model_cover,
        model_qa=model_qa
    )
    return output["cv"], output["cover_letter"], output["review"]

def generate_profile(profile_text):
    profile_data = OllamaClient().generate(
        prompt=f"Extract structured profile information in JSON format from the following input:\n{profile_text}\n\nRespond only with JSON.")
    try:
        profile_manager.save(profile_data)
        return "Profile saved successfully!"
    except Exception as e:
        return f"Error saving profile: {e}"

def main():
    models = get_available_models()
    with gr.Blocks() as demo:
        with gr.Tab("Generate CV & Cover Letter"):
            gr.Markdown("# AI-Powered CV and Cover Letter Generator")
            job_input = gr.Textbox(label="Job Description", placeholder="Paste job description here")

            model_cv_input = gr.Dropdown(label="Model for CV Writer", choices=models, value=models[0])
            model_cover_input = gr.Dropdown(label="Model for Cover Letter", choices=models, value=models[0])
            model_qa_input = gr.Dropdown(label="Model for QA Reviewer", choices=models, value=models[0])

            btn = gr.Button("Generate")

            cv_output = gr.Textbox(label="Generated CV")
            cover_output = gr.Textbox(label="Generated Cover Letter")
            review_output = gr.Textbox(label="QA Review")

            btn.click(
                fn=generate_docs,
                inputs=[job_input, model_cv_input, model_cover_input, model_qa_input],
                outputs=[cv_output, cover_output, review_output]
            )

        with gr.Tab("Build Profile"):
            gr.Markdown("# Profile Builder")
            profile_text_input = gr.Textbox(label="Describe your background, experience, skills, etc.", lines=10)
            save_btn = gr.Button("Generate & Save Profile")
            profile_status = gr.Textbox(label="Status")

            save_btn.click(
                fn=generate_profile,
                inputs=[profile_text_input],
                outputs=[profile_status]
            )

    demo.launch()

if __name__ == "__main__":
    main()
