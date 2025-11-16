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
```

## Usage

## Optional: Create alias

Add to `.bashrc` or `.zshrc`:
```bash
alias nn='python ~/path/to/notion_note.py'
```

### Create new pages

```bash
nn "Title" "Content"                    # create page with content
nn "Title" -f file.txt                  # create page from file
```

### Add to existing pages

```bash
nn --list                               # list recent pages with IDs
nn -p PAGE_ID "More content"            # append to existing page
nn -p PAGE_ID -f notes.txt              # append file to existing page
```

### Get Page ID

**Option 1:** List pages
```bash
nn --list
```

**Option 2:** From URL
```
https://www.notion.so/workspace/...?p=a1b2c3d4e5f6&pm=s
                                      ^^^^^^^^^^^^^^^^
                                      This is your Page ID
```

## Workflow Example

```bash
# Day 1: Create study page
nn "Python Recursion" "Starting to learn recursion"

# List pages to get ID
nn --list
# Output: ID: a1b2c3d4e5f6

# Day 2: Add more notes to same page
nn -p a1b2c3d4e5f6 "Factorial example: n * factorial(n-1)"

# Day 3: Add exercise file
nn -p a1b2c3d4e5f6 -f exercises.txt
```
