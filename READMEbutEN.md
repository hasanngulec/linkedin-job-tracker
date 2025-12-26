# 📊 LinkedIn Job Application Tracker

A platform that automatically fetches and analyzes your LinkedIn job applications.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)
![n8n](https://img.shields.io/badge/n8n-Automation-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🔄 Part 1: n8n Automation

The n8n workflow automatically fetches LinkedIn application emails from Gmail, categorizes them, and saves them to Google Sheets.

### 📋 Workflow Structure

```
Manual Trigger → Gmail → Categorize & Extract Data → Filter → Google Sheets
```

### 🔧 Workflow Nodes

| Node | Description |
|------|-------------|
| **Manual Trigger** | Manually starts the workflow |
| **Gmail** | Fetches emails from LinkedIn (linkedin.com sender filter) |
| **Categorize & Extract Data** | Analyzes emails, extracts company/position/status info |
| **Filter** | Filters only job application emails |
| **Google Sheets** | Saves data to Google Sheets |

### 📧 Email Categories

The workflow categorizes emails into the following:

| Category | Status | Trigger Keywords |
|----------|--------|-----------------|
| `application_submitted` | Applied | "application was sent", "your application to" |
| `application_viewed` | Under Review | "application was viewed" |
| `interview_invite` | Interview | "interview" |
| `rejected` | Rejected | "unfortunately", "not moving forward" |

### ⚙️ n8n Setup

1. Create an [n8n](https://n8n.io/) account (cloud or self-hosted)
2. Import the `applications.json` file into n8n
3. Configure credentials:

#### Gmail OAuth2 Credential
```
1. Create OAuth 2.0 credential in Google Cloud Console
2. Enable Gmail API
3. Add Gmail OAuth2 credential in n8n
4. Update YOUR_GMAIL_CREDENTIAL_ID and YOUR_GMAIL_CREDENTIAL_NAME in the workflow
```

#### Google Sheets OAuth2 Credential
```
1. Create OAuth 2.0 credential in Google Cloud Console
2. Enable Google Sheets API
3. Add Google Sheets OAuth2 credential in n8n
4. Update YOUR_GOOGLE_SHEETS_CREDENTIAL_ID and YOUR_GOOGLE_SHEETS_CREDENTIAL_NAME in the workflow
```

4. Update your Google Sheets URL:
   - `YOUR_GOOGLE_SHEETS_URL` → Your own Google Sheets link

### 📊 Google Sheets Columns

The workflow creates these columns:

| Column | Description |
|--------|-------------|
| Date | Application date |
| Time | Application time |
| Company | Company name |
| Position | Position title |
| Category | Category code |
| Status | Status |
| Subject | Email subject |
| Gmail Link | Direct link to email in Gmail |
| Processed At | Processing timestamp |

### ▶️ Running the Workflow

1. Open the workflow in n8n
2. Click "Execute Workflow" button
3. Emails are fetched from Gmail and processed
4. Data is saved to Google Sheets
5. Export as CSV from Google Sheets

---

## 📈 Part 2: Streamlit Dashboard

The Streamlit dashboard visualizes and analyzes data from n8n.

### 🎯 Features

- **Metric Cards**: Total applications, interviews, rejection rate
- **Status Distribution**: Pie chart visualization
- **Time Trend**: Daily application chart + 7-day moving average
- **Company Analysis**: Most applied companies
- **Position Analysis**: Popular positions
- **Weekly/Monthly Histogram**: Periodic activity
- **Response Funnel**: Application → View → Interview flow
- **Filtering**: Date, status, company-based filtering
- **HTML Export**: Download all analyses in one file

### 🚀 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### 📋 Usage

1. **CSV Upload**: Upload your CSV from n8n via the left panel
2. **Demo Mode**: "Use demo data" option to test without CSV
3. **Filtering**: Date range, status, and company filters
4. **Export**: Download as CSV or HTML dashboard

### 🎨 Dashboard Sections

#### Overview
- Total application count
- Unique company count
- Interview invitation count
- Under review count
- Rejection rate

#### Detailed Analytics
- Application status distribution (pie chart)
- Application response funnel
- Daily application trend
- Most applied companies (bar chart)
- Most applied positions
- Weekly/Monthly histogram (selectable)
- Company-based status distribution

#### Application Details
- Table view (first 50 records)
- Direct email access via Gmail link

### 📊 Data Format

The dashboard expects this CSV format:

```csv
Date,Company,Position,Category,Status,Subject,Gmail Link,Processed At
2025-01-15,Company A,Position 1,application_submitted,Applied,Your application...,https://mail...,2025-01-15T10:30:00.000Z
```

### 🖥️ HTML Dashboard Export

Download an interactive HTML file containing all analyses with the "Download Dashboard" button:
- All charts (Plotly interactive)
- Metric cards
- Detailed table
- Print-friendly design

---

## 📁 Project Structure

```
linkedin_basvurular/
├── app.py              # Streamlit dashboard application
├── applications.json   # n8n workflow file
├── sample_data.csv     # Sample dataset (anonymous)
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore file
├── README.md           # Turkish documentation
└── READMEbutEN.md      # English documentation (this file)
```

---

## 🔐 Security Notes

- Credential IDs in `applications.json` are placeholder values
- Do not upload your real application data to GitHub
- `.gitignore` automatically ignores sensitive data
- `sample_data.csv` is completely anonymous sample data

---

## 🤝 Contributing

1. Fork this repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push your branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Technologies

- [n8n](https://n8n.io/) - Workflow automation platform
- [Streamlit](https://streamlit.io/) - Python dashboard framework
- [Plotly](https://plotly.com/) - Interactive charts
- [Pandas](https://pandas.pydata.org/) - Data analysis

---

⭐ Don't forget to star this project if you found it useful!

