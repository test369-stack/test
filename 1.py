import requests
import base64

token = ''
username = 'test369-stack'
repo_name = 'test'

headers = {
    'Authorization': f'token {token}',
    'Content-Type': 'application/json'
}

# Step 1: Create a new repository
repo_url = 'https://api.github.com/user/repos'
repo_data = {
    "name": repo_name,
    "private": False
}
response = requests.post(repo_url, json=repo_data, headers=headers)

if response.status_code == 201:
    print(f"Repository '{repo_name}' created successfully!")
else:
    print(f"Failed to create repository: {response.json()}")

# Step 2: Create a file blob
content = "Hello, GitHub!"
content_encoded = base64.b64encode(content.encode()).decode()

blob_url = f'https://api.github.com/repos/{username}/{repo_name}/git/blobs'
blob_data = {
    "content": content_encoded,
    "encoding": "base64"
}
blob_response = requests.post(blob_url, json=blob_data, headers=headers)
blob_sha = blob_response.json().get('sha')

# Step 3: Create a tree
tree_url = f'https://api.github.com/repos/{username}/{repo_name}/git/trees'
tree_data = {
    "tree": [
        {
            "path": "hello.txt",
            "mode": "100644",
            "type": "blob",
            "sha": blob_sha
        }
    ]
}
tree_response = requests.post(tree_url, json=tree_data, headers=headers)
tree_sha = tree_response.json().get('sha')

# Step 4: Create a commit
commit_url = f'https://api.github.com/repos/{username}/{repo_name}/git/commits'
commit_data = {
    "message": "Initial commit",
    "tree": tree_sha,
    "parents": []
}
commit_response = requests.post(commit_url, json=commit_data, headers=headers)
commit_sha = commit_response.json().get('sha')

# Step 5: Push commit to main branch
ref_url = f'https://api.github.com/repos/{username}/{repo_name}/git/refs/heads/main'
ref_data = {
    "sha": commit_sha
}
ref_response = requests.patch(ref_url, json=ref_data, headers=headers)

print("Commit pushed successfully!")