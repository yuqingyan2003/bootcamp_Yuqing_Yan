 #!/usr/bin/env python3
"""
Create DAG diagram for AAPL Pipeline
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Define tasks and positions
tasks = [
    ('data_ingestion', 'Data Ingestion\n(yfinance API)', (2, 6)),
    ('data_cleaning', 'Data Cleaning\n(normalize, validate)', (2, 5)),
    ('feature_engineering', 'Feature Engineering\n(technical indicators)', (2, 4)),
    ('model_training', 'Model Training\n(Linear/Logistic Regression)', (2, 3)),
    ('model_evaluation', 'Model Evaluation\n(metrics, diagnostics)', (2, 2)),
    ('reporting', 'Reporting\n(stakeholder analysis)', (2, 1))
]

# Colors for different task types
colors = {
    'data_ingestion': '#E8F4FD',      # Light blue
    'data_cleaning': '#E8F6F3',       # Light green  
    'feature_engineering': '#FDF2E9', # Light orange
    'model_training': '#F4ECF7',      # Light purple
    'model_evaluation': '#FADBD8',    # Light red
    'reporting': '#EAEDED'            # Light gray
}

# Draw task boxes
box_width = 2.5
box_height = 0.6
boxes = {}

for task_id, task_name, (x, y) in tasks:
    # Create fancy box
    box = FancyBboxPatch(
        (x - box_width/2, y - box_height/2), 
        box_width, box_height,
        boxstyle="round,pad=0.1",
        facecolor=colors[task_id],
        edgecolor='#2C3E50',
        linewidth=2
    )
    ax.add_patch(box)
    boxes[task_id] = (x, y)
    
    # Add task text
    ax.text(x, y, task_name, ha='center', va='center', 
           fontsize=10, fontweight='bold', wrap=True)

# Draw arrows between tasks
arrow_props = dict(
    arrowstyle='->', 
    color='#2C3E50', 
    lw=2,
    connectionstyle="arc3,rad=0"
)

# Define connections (linear pipeline)
connections = [
    ('data_ingestion', 'data_cleaning'),
    ('data_cleaning', 'feature_engineering'),
    ('feature_engineering', 'model_training'),
    ('model_training', 'model_evaluation'),
    ('model_evaluation', 'reporting')
]

for source, target in connections:
    source_x, source_y = boxes[source]
    target_x, target_y = boxes[target]
    
    # Draw arrow from bottom of source to top of target
    ax.annotate('', 
                xy=(target_x, target_y + box_height/2), 
                xytext=(source_x, source_y - box_height/2),
                arrowprops=arrow_props)

# Add timing annotations
timings = [
    ('data_ingestion', '2-5 min'),
    ('data_cleaning', '1-2 min'),
    ('feature_engineering', '2-3 min'),
    ('model_training', '5-10 min'),
    ('model_evaluation', '3-5 min'),
    ('reporting', '2-3 min')
]

for task_id, timing in timings:
    x, y = boxes[task_id]
    ax.text(x + box_width/2 + 0.3, y, timing, ha='left', va='center',
           fontsize=9, style='italic', color='#7F8C8D')

# Add title and labels
ax.set_title('AAPL Stock Prediction Pipeline - Task Dependencies (DAG)', 
             fontsize=16, fontweight='bold', pad=20)

# Add legend for task types
legend_elements = [
    mpatches.Patch(color=colors['data_ingestion'], label='Data Ingestion'),
    mpatches.Patch(color=colors['data_cleaning'], label='Data Processing'),
    mpatches.Patch(color=colors['feature_engineering'], label='Feature Engineering'),
    mpatches.Patch(color=colors['model_training'], label='Model Training'),
    mpatches.Patch(color=colors['model_evaluation'], label='Model Evaluation'),
    mpatches.Patch(color=colors['reporting'], label='Reporting')
]

ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))

# Add pipeline characteristics
ax.text(0.5, 0.5, 
        'Pipeline Characteristics:\n' +
        '• Linear dependency chain\n' +
        '• Total runtime: ~15-28 minutes\n' +
        '• 6 sequential tasks\n' +
        '• No current parallelization\n' +
        '• Checkpoint recovery enabled',
        ha='left', va='center', fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor='#F8F9FA', edgecolor='#BDC3C7'))

# Set axis properties
ax.set_xlim(0, 6)
ax.set_ylim(0.5, 6.5)
ax.set_aspect('equal')
ax.axis('off')

# Save the diagram
plt.tight_layout()
plt.savefig('aapl_pipeline_dag.png', dpi=300, bbox_inches='tight')
plt.savefig('aapl_pipeline_dag.pdf', bbox_inches='tight')

print("DAG diagram saved as:")
print("- aapl_pipeline_dag.png")
print("- aapl_pipeline_dag.pdf")

plt.show()