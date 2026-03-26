import json
import os
import sys

tmp_files = [f for f in os.listdir("tmp") if f.endswith(".json")]

overwrites = []
for f in tmp_files:
    path = os.path.join("tmp", f)
    with open(path) as fh:
        data = json.load(fh)

    leaderboard_results = data.get("leaderboard_results", {})
    agent_name = leaderboard_results.get("agent_name")
    model_id = leaderboard_results.get("model_id")
    level_id = leaderboard_results.get("level_id")

    if not agent_name:
        raise ValueError(f"Missing agent_name in {path}")
    if not level_id:
        raise ValueError(f"Missing level_id in {path}")
    if not model_id:
        raise ValueError(f"Missing model_id in {path}")

    task_path = os.path.join("data", f"{level_id}.json")
    if not os.path.exists(task_path):
        continue

    with open(task_path) as fh:
        task_data = json.load(fh)

    entries = task_data.get("entries", [])
    if any(e.get("agent_name") == agent_name and e.get("model_id") == model_id for e in entries):
        overwrites.append((level_id, agent_name, model_id, f))

allow_overwrite = True
if overwrites:
    print("The following entries will be overwritten:")
    for level_id, agent_name, model_id, source_file in overwrites:
        print(f"- {level_id}: {agent_name} with {model_id} (from {source_file})")
    response = input(
        "\nATTENTION: ABOUT TO OVERWRITE EXISTING ENTRIES\n\n"
        "Proceed with overwriting these entries?\n\n"
        "Type 'y' to proceed. Default is no [y/N]: "
    ).strip().lower()
    allow_overwrite = response in ("y", "yes")
    if not allow_overwrite:
        sys.exit(0)

for f in tmp_files:
    path = os.path.join("tmp", f)
    print(f"Processing {path}...")
    with open(path) as fh:
        data = json.load(fh)

        leaderboard_results = data.get("leaderboard_results", {})

        agent_name = leaderboard_results.get("agent_name")
        model_id = leaderboard_results.get("model_id")
        website_url = leaderboard_results.get("website_url")
        timestamp = leaderboard_results.get("timestamp")
        date = timestamp.split("_")[0] if timestamp else None
        num_seeds = leaderboard_results.get("num_seeds")
        level_id = leaderboard_results.get("level_id")
        mean_final_success_rate = leaderboard_results.get("mean_final_success_rate")
        mean_final_progress = leaderboard_results.get("mean_final_progress")
        std_final_success_rate = leaderboard_results.get("std_final_success_rate")
        std_final_progress = leaderboard_results.get("std_final_progress")
        mean_num_episodes = leaderboard_results.get("mean_num_episodes")
        std_num_episodes = leaderboard_results.get("std_num_episodes")

        entry = {
            "agent_name": agent_name,
            "model_id": model_id,
            "website_url": website_url,
            "date": date,
            "num_seeds": num_seeds,
            "level_id": level_id,
            "mean_final_success_rate": mean_final_success_rate,
            "mean_final_progress": mean_final_progress,
            "std_final_success_rate": std_final_success_rate,
            "std_final_progress": std_final_progress,
            "mean_num_episodes": mean_num_episodes,
            "std_num_episodes": std_num_episodes,
        }

        if level_id:
            os.makedirs("data", exist_ok=True)
            tasks_path = os.path.join("data", "tasks.json")
            if os.path.exists(tasks_path):
                with open(tasks_path) as fh:
                    tasks_data = json.load(fh)
            else:
                tasks_data = {"tasks": []}

            if level_id not in tasks_data.get("tasks", []):
                tasks_list = tasks_data.setdefault("tasks", [])
                tasks_list.append(level_id)
                tasks_list.sort(key=lambda x: (int(x.split('-')[1]), int(x.split('-')[3])))
                
                with open(tasks_path, "w") as fh:
                    json.dump(tasks_data, fh, indent=2)

            task_path = os.path.join("data", f"{level_id}.json")
            if os.path.exists(task_path):
                with open(task_path) as fh:
                    task_data = json.load(fh)
            else:
                task_data = {"level_id": level_id, "entries": []}

            entries = task_data.setdefault("entries", [])
            
            existing_index = next(
                (i for i, e in enumerate(entries) if e.get("agent_name") == agent_name and e.get("model_id") == model_id),
                None,
            )
            if existing_index is not None:
                entries.pop(existing_index)
            
            # Append the new entry
            entries.append(entry)
            
            # Sort the list by mean_final_success_rate in descending order
            entries.sort(
                key=lambda x: x.get("mean_final_success_rate", float('-inf')), 
                reverse=True
            )

            with open(task_path, "w") as fh:
                json.dump(task_data, fh, indent=2)
        else:
            print("Skipping write: missing level_id")