import os
import json
import frontmatter
from datetime import datetime
from subprocess import check_output

def get_modified_files():
		# Get the list of modified and newly created markdown files
	# Modified files since the last commit
	modified_output = check_output(["git", "diff", "--name-status", "HEAD^", "HEAD"]).decode("utf-8")
	
	# Staged files (includes newly created)
	staged_output = check_output(["git", "diff", "--cached", "--name-status"]).decode("utf-8")

	# Combine both outputs
	files = modified_output + staged_output
	
	# Process the combined output
	file_statuses = [line.strip().split('\t') for line in files.split('\n') if line.endswith(".md")]

	# Convert list of lists to a list of tuples for set operations
	file_statuses_tuples = [tuple(status) for status in file_statuses]
	
	# Remove duplicates by converting to a set and back to a list
	unique_files = list(set(file_statuses_tuples))
	
	# Convert back to list of lists if needed
	unique_files = [list(item) for item in unique_files]
	print(unique_files)
	
	return unique_files

def process_markdown_files(files, json_file):
	if os.path.exists(json_file):
		with open(json_file, 'r') as f:
			data = json.load(f)
	else:
		data = []

	# Create a dictionary for quick lookup based on file path
	data_dict = {item.get("file_path"): item for item in data}

	for status, md_file in files:
		try:
			with open(md_file, 'r', encoding='utf-8') as f:
				post = frontmatter.loads(f.read())
		except Exception as e:
			print(f"Error processing {md_file}: {e}")
			continue

		title = post.get("title", "Untitled")
		tags = post.get("tags", [])

		if status == 'A':  # File is newly added
			entry = {
				"date": datetime.now().strftime('%Y-%m-%d'),
				"title": title,
				"tags": tags,
				"file_path": md_file,
				"frontmatter": post.metadata
			}
			data_dict[md_file] = entry
		elif status == 'M':  # File is modified
			if md_file in data_dict:
				data_dict[md_file]["title"] = title
				data_dict[md_file]["tags"] = tags
				data_dict[md_file]["frontmatter"] = post.metadata

	# Convert dictionary back to list
	data = list(data_dict.values())

	# Write updated data back to the JSON file
	with open(json_file, 'w', encoding='utf-8') as f:
		json.dump(data, f, indent=4)

if __name__ == "__main__":
	modified_files = get_modified_files()
	output_json = "./metadata.json"  # JSON file to be updated
	
	if modified_files:
		process_markdown_files(modified_files, output_json)
	else:
		print("No modified markdown files to process.")
