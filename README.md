# BuilderBench Leaderboard

This repo hosts the BuilderBench leaderboard at [builderbench-leaderboard.github.io](https://builderbench-leaderboard.github.io). All leaderboard data lives as plain JSON files under `data/`. To add results, you generate a `tmp/` folder containing your results from the [builderbench](https://github.com/RajGhugare19/builderbench) repo, drop it here, and simply run one script. The instructions on how to run your agent and get the results in a `tmp/` folder can be found in the [builderbench](https://github.com/RajGhugare19/builderbench) repo.

---

## How to submit results

### Step 1 — Run your agent and generate the `tmp/` folder

This happens in the **builderbench** repo, not this one. After you've run your agent and have results under `outputs/`, use `submit.py` to package them:

```bash
python submit.py \
    --results_dir outputs/ \
    --level_id cube-5-task-3 \
    --model_id your-model-id \
    --agent_name your-agent-name \
    --website_url https://your-project-url   # optional
```

Run this once per task. Each call writes one file to `tmp/<level_id>-leaderboard.json`. To submit all tasks at once, see the [example script in builderbench repo](https://github.com/RajGhugare19/builderbench/blob/main/scripts/submit_claude_opus4.6.sh) — it loops over all tasks and calls `submit.py` for each.

When you're done, you'll have a `tmp/` folder that looks like:

```
tmp/
  cube-1-task-1-leaderboard.json
  cube-2-task-3-leaderboard.json
  ...
```

### Step 2 — Clone this repo and drop in the `tmp/` folder

```bash
git clone https://github.com/RajGhugare19/builderbench-leaderboard.github.io
cd builderbench-leaderboard.github.io
```

Copy your `tmp/` folder from the builderbench repo into the root of this repo:

```bash
cp -r /path/to/builderbench/tmp ./tmp
```

### Step 3 — Run `place_data.py`

```bash
python place_data.py
```

This script reads every JSON file in `tmp/`, validates that `agent_name`, `model_id`, and `level_id` are present, and merges the results into the appropriate file under `data/`. It also updates `data/tasks.json` if a task is new.

If your agent + model combination already exists for a task, it will ask before overwriting:

```
The following entries will be overwritten:
- cube-5-task-3: my-agent with my-model-id (from cube-5-task-3-leaderboard.json)

ATTENTION: ABOUT TO OVERWRITE EXISTING ENTRIES

Proceed with overwriting these entries?

Type 'y' to proceed. Default is no [y/N]:
```

Type `y` to proceed, or press Enter to abort.

### Step 4 — Open a pull request

```bash
git checkout -b submit/your-agent-name
git add data/
git commit -m "Add results: your-agent-name on your-model-id"
git push origin submit/your-agent-name
```

Then open a PR against `main`. Once merged, the leaderboard updates automatically via GitHub Pages.

---

## Repo structure

```
data/
  tasks.json              # ordered list of all task IDs
  cube-1-task-1.json      # per-task leaderboard entries
  cube-2-task-3.json
  ...
place_data.py             # merges tmp/ into data/
index.html                # the leaderboard page
```

`place_data.py` is the only script you need to run in this repo. Everything else is managed by GitHub Pages.
