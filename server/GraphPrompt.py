graph_prompt = """
Please analyze the following report and generate a JSON file containing graphs that can be plotted using the provided Python function. Follow these instructions carefully:

---

Objective

Identify interesting and meaningful insights from the report and represent them using appropriate graphs.

Graph Requirements

1. Graph Types

   You may only choose from the following graph types:

   - Bar Graph
   - Line Graph
   - Pie Chart

2. Headings

   Each graph must be associated with one of the following headings:

   - Sector Overview
   - Competitive Landscape
   - Product and Service Offerings
   - Customer Segmentation
   - Financial Performance
   - Market Opportunities
   - Regulatory and Compliance Landscape
   - Recommendations for New Entrants

3. Data Points

   - Source

     All data points must be present in the report. You are not allowed to make up data points.

   - Validity

     Only include meaningful data points. Omit any data that does not make sense or has missing values. For example, if a value sequence goes from 200 million to 300 million to 1 million without explanation, omit the 1 million.

   - Completeness

     If you have missing values in a sequence (e.g., missing the year 2025 in a yearly series), you may omit the incomplete data point.

Graph Selection Criteria

- Appropriateness

  - Use a Bar Graph for discrete values.
  - Use a Line Graph for continuous values.
  - Use a Pie Chart to represent parts of a whole.

- Uniqueness

  Do not generate multiple graphs that convey the same information. Each graph should provide a different insight.

JSON Output Format

Provide the output in a single JSON file with the following structure:

{
  "graphs": [
    {
      "heading": "Sector Overview",
      "type": "Bar Graph",
      "data": {
        "x_axis": {
          "label": "Year",
          "values": [2023, 2024, 2025, 2026]
        },
        "y_axis": {
          "label": "Market Size (USD Million)",
          "values": [619.3, 764.1, 942.4, 1160.5]
        }
      }
    },
    {
      "heading": "Financial Performance",
      "type": "Line Graph",
      "data": {
        "x_axis": {
          "label": "Year",
          "values": [2024, 2025, 2026, 2027, 2028]
        },
        "y_axis": {
          "label": "Healthcare Spending (% of GDP)",
          "values": [5.4, 5.8, 6.3, 6.8, 7.2]
        }
      }
    }
  ]
}

Compatibility with Python Function
  Ensure that the JSON output is compatible with the following Python plotting function:

def plot_graphs(json_output):
  for graph in json_output['graphs']:
      graph_type = graph['type']
      x_values = graph['data']['x_axis']['values']
      y_values = graph['data']['y_axis']['values']
      x_label = graph['data']['x_axis']['label']
      y_label = graph['data']['y_axis']['label']

      plt.figure()

      if graph_type == "Bar Graph":
          plt.bar(x_values, y_values, color='teal')
      elif graph_type == "Line Graph":
          plt.plot(x_values, y_values, marker='o', color='steelblue')
      elif graph_type == "Pie Chart":
          plt.pie(y_values, labels=x_values, autopct='%1.1f%%', colors=['peru', 'peachpuff', 'coral', 'lightgreen'])

      plt.title(graph_type)
      plt.xlabel(x_label)
      plt.ylabel(y_label)

      plt.show()

Exclusion
  Do not include any graphs that are not compatible with this function.

Output Instructions
  Exclusivity
    Do not output anything other than the JSON output.

  Accuracy
    Ensure that all data used in the graphs is accurate and sourced directly from the report.

  Formatting
    The JSON file must be properly formatted and free of errors to ensure compatibility with the plotting function.

The graph you select must be appropriate for the data points you have chosen. For example, if you have data points for the market size over the years, you may choose a bar graph or a line graph. If you have data points for the market share of different companies, you may choose a pie chart.
If you have missing values, you may omit the data points. For example, if you have data points for the market size for the years 2023, 2024, 2026, and 2027, you may omit the year 2025.
For discrete values, you may only choose a bar graph. For continuous values, you may only choose a line graph.

Do NOT generate multiple graphs that convey the same information. Try to analyze and generate graphs that convey different insights.

If the data is not sufficient to generate meaningful graphs, you may omit the graph.
If the data is not up to date or up to the mark, you may omit the graph.
If there is any ambiguity in the data, you may omit the graph.
Never provide a null value. In case of null value, provide a mean or median value
If there is not enough information to strongly attest the data, you may omit the graph.

Markdown Content below this line

---

"""
