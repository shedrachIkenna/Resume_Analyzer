from utils.file_reader import read_resume_text

def main():
    file_path = 'resume/sample_resume.txt'
    resume_text = read_resume_text(file_path)
    print(f"\n===== Resume Content =====")
    print(resume_text)


if __name__ == "__main__":
    main()