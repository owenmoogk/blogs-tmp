import os
import json
import frontmatter
from datetime import datetime
from subprocess import check_output

def get_modified_files():
	# Get the list of modified and newly created markdown files
	output = check_output(["git", "diff", "--name-status", "HEAD^", "HEAD"]).decode("utf-8")
	files = [line.strip().split('\t') for line in output.split("\n") if line.endswith(".md")]
	return files

def process_markdown_files(files, json_file):

	if os.path.exists(json_file):
		with open(json_file, 'r') as f:
			data = json.load(f)
	else:
		data = []


	# Create a dictionary for quick lookup
	data_dict = {item.get("title"): item for item in data}

	for status, md_file in files:
		try:
			with open(md_file, 'r', encoding='utf-8') as f:
				post = frontmatter.loads(f.read())
		except Exception as e:
			print(f"Error processing {md_file}: {e}")
			continue
		print(status, md_file)
		title = post.get("title", "Untitled")
		tags = post.get("tags", [])
		
		if status == 'A':  # File is newly added
			entry = {
				"date": datetime.now().strftime('%Y-%m-%d'),
				"title": title,
				"tags": tags,
			}
			data_dict[title] = entry
		elif status == 'M':  # File is modified
			if title in data_dict:
				print("HERE")
				data_dict[title]["title"] = title
				data_dict[title]["tags"] = tags

	# Convert dictionary back to list
	data = list(data_dict.values())
	print(data)

	# Write updated data back to the JSON file
	with open(json_file, 'w', encoding='utf-8') as f:
		json.dump(data, f, indent=4)

if __name__ == "__main__":
	modified_files = get_modified_files()
	print(modified_files)
	output_json = "./metadata.json"  # JSON file to be updated
	
	if modified_files:
		process_markdown_files(modified_files, output_json)
	else:
		print("No modified markdown files to process.")
