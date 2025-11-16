# nn - terminal notes to notion

<div align=center>
  <img src="https://i.ibb.co/JW7662XY/nn.png" width=35%>
</div>

Quick Python script to send notes from your terminal directly to Notion.

## Setup

### 1. Create Notion Integration

1. Go to https://www.notion.so/profile/integrations
2. Click **"+ New integration"**
3. Give it a name (e.g., "nn terminal")
4. Copy the **Internal Integration Token**
5. Paste it in the script: `NOTION_TOKEN = "your_token_here"`

### 2. Create Database

1. Open Notion and create a new page
2. Type `/table` and select **"Table - Inline"**
3. The database is created with a "Name" column (required)

### 3. Connect Integration to Database

1. Open your database page
2. Click **"..."** (top right) → **"Connections"**
3. Add your integration

### 4. Get Database ID

1. Open the database in your browser
2. Copy the ID from the URL:
```
https://www.notion.so/workspace/a1b2c3d4e5f6...?v=...
                              ^^^^^^^^^^^^^^^^
                              This is your Database ID
```
3. Paste it in the script: `DATABASE_ID = "your_database_id_here"`

### 5. Install & Run

```bash
pip install requests
python notion_note.py --check  # verify columns
python notion_note.py "Title" "Content"
python notion_note.py "Title" -f file.txt
```

### Optional: Create alias

Add to `.bashrc` or `.zshrc`:
```bash
alias nn='python ~/path/to/notion_note.py'
```

Now just: `nn "Title" "Content"`

---
