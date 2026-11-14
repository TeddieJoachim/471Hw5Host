import csv
import matplotlib.pyplot as plt

# load experiment data

experiments = {
  "Predator + Moving Feeder": ("forceWPredWfeederMove.csv", True),
  "No Predator + Stationary Feeder": ("forceNoPredNoMove.csv", False),
  "Predator + Stationary Feeder": ("forceWPredNoMove.csv", True),
}

data = {}

for name, (filename, has_predator) in experiments.items():
  with open(filename, "r") as file:
    reader = csv.DictReader(file)
    data[name] = {
      "rows": list(reader),
      "has_predator": has_predator
    }


# calculate mean force magnitudes across flock

summary = {}

for name, experiment in data.items():
  rows = experiment["rows"]
  has_predator = experiment["has_predator"]

  # if there is a predator, exclude it from the flock average
  predator_id = max(int(row["bird_id"]) for row in rows) if has_predator else None

  time_groups = {}

  for row in rows:
    bird_id = int(row["bird_id"])

    if has_predator and bird_id == predator_id:
      continue

    t = float(row["time"])

    if t not in time_groups:
      time_groups[t] = {
        "cohesion": [],
        "repulsion": [],
        "follow": [],
        "predator": [],
      }

    for column in time_groups[t]:
      time_groups[t][column].append(float(row[column]))

  stats = {}

  for t, forces in time_groups.items():
    stats[t] = {
      "mean_cohesion": sum(forces["cohesion"]) / len(forces["cohesion"]),
      "mean_repulsion": sum(forces["repulsion"]) / len(forces["repulsion"]),
      "mean_follow": sum(forces["follow"]) / len(forces["follow"]),
      "mean_predator_force": sum(forces["predator"]) / len(forces["predator"]),
    }

  summary[name] = stats


# individual force components

force_columns = [
  ("mean_cohesion", "Cohesion"),
  ("mean_repulsion", "Neighbor Repulsion"),
  ("mean_follow", "Leader Following"),
  ("mean_predator_force", "Predator Avoidance")
]

fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True)

for ax, (column, title) in zip(axes.flat, force_columns):
  for name, stats in summary.items():
    times = sorted(stats.keys())
    ax.plot(times, [stats[t][column] for t in times], label=name)

  ax.set_title(title)
  ax.set_xlabel("Simulation Time")
  ax.set_ylabel("Mean Force Magnitude")
  ax.legend()
  ax.grid()

plt.tight_layout()
plt.savefig("force_components.png", dpi=300)
plt.show()