# Daily Naukri Profile Updater 🚀

Automated Python script designed to run daily to keep your Naukri profile "active" and appearing at the top of recruiter searches. 

Recruiters regularly filter candidates on job portals like Naukri using the **"Last Active"** filter. This automation simulates a login and makes a safe, minor adjustment to your resume headline daily, which flags your profile as recently updated.

---

## 🛠️ Local Setup (for Testing)

1. **Clone or copy this directory** to your local machine.
2. **Install Python 3.8+** if you don't have it.
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
4. **Create a `.env` file** in the root directory:
   ```env
   NAUKRI_USERNAME=your_email@example.com
   NAUKRI_PASSWORD=your_secure_password
   ```
5. **Run the script**:
   ```bash
   python updater.py
   ```
   *If successful, it will print progress messages and confirm the save. If it fails, check the generated `naukri_error_screenshot.png` to see what went wrong.*

---

## 🚀 GitHub Actions Setup (Automatic Daily Runs)

To automate this so it runs daily at **10:00 AM IST** without keeping your computer on, set it up on GitHub:

### 1. Create a GitHub Repository
* Go to GitHub and create a **NEW repository**.
* ⚠️ **IMPORTANT**: Make sure the repository is set to **PRIVATE** to protect your code and execution logs.
* Push this project to your repository.

### 2. Configure Credentials (Secrets)
* In your GitHub repository, navigate to **Settings** > **Secrets and variables** > **Actions**.
* Click on **New repository secret**.
* Add the following secrets:
  * **Name**: `NAUKRI_USERNAME` | **Value**: *Your Naukri Email ID / Username*
  * **Name**: `NAUKRI_PASSWORD` | **Value**: *Your Naukri Password*

### 3. Run and Monitor
* Go to the **Actions** tab in your GitHub repository.
* Select **Naukri Daily Profile Updater** from the left sidebar.
* Click the **Run workflow** dropdown and press the green button to trigger a test run immediately.
* Under the cron schedule, it will trigger automatically every day at **10:00 AM IST** (4:30 AM UTC).

### 🔍 Troubleshooting
* If the run fails on GitHub Actions, the workflow is configured to save a screenshot of the browser page at the exact moment of failure. 
* Go to the failed workflow run details page, scroll down to the **Artifacts** section, and download `error-screenshot` to inspect the visual issue (e.g., Captcha request, layout change, or incorrect password).
