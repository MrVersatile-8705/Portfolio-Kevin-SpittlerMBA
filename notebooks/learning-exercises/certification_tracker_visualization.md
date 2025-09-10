# Creating Certification Tracker Visualizations in Excel

## Step 1: Prepare Your Data in Excel

### A. Create the Base Table
```
Certification                                    | Platform        | Status        | Target Date    | Progress %
Google Data Analytics Professional               | Coursera        | In Progress   | March 2025     | 75
Microsoft Power BI Data Analyst Professional    | Coursera        | In Progress   | October 2025   | 40
Azure Data Engineer Associate                    | Microsoft Learn | Planned       | May 2025       | 0
Python for Data Science                         | Coursera        | Planned       | April 2025     | 0
Tableau Desktop Specialist                      | Tableau         | Completed     | January 2021   | 100
dbt Fundamentals                                | dbt Labs        | Planned       | November 2025  | 0
```

### B. Add Helper Columns for Visualization
1. **Status Number**: Convert status to numbers for charts
   - Completed = 3
   - In Progress = 2
   - Planned = 1

2. **Days to Completion**: Calculate days remaining
   ```excel
   =IF(Status="Completed", 0, Target_Date - TODAY())
   ```

3. **Category**: Group by skill type
   - Analytics: Google Data Analytics, Power BI
   - Engineering: Azure Data Engineer, dbt
   - Programming: Python
   - Visualization: Tableau

## Step 2: Create Visual Charts

### Chart 1: Progress by Certification (Horizontal Bar Chart)
1. Select certification names and progress percentages
2. Insert → Charts → Bar Chart
3. Format with colors: Red (0-33%), Yellow (34-66%), Green (67-100%)

### Chart 2: Timeline Gantt Chart
1. Create start dates, duration, and completion dates
2. Use stacked bar chart to show timeline
3. Format bars to show current progress vs. remaining time

### Chart 3: Status Distribution (Pie Chart)
1. Count certifications by status
2. Insert → Charts → Pie Chart
3. Use your brand colors for segments

### Chart 4: Platform Distribution (Donut Chart)
1. Count certifications by platform
2. Insert → Charts → Doughnut Chart
3. Add data labels with percentages

## Step 3: Create Dashboard Layout
1. Arrange charts on one worksheet
2. Add title: "Professional Development Dashboard"
3. Include summary statistics
4. Add your name and update date

## Excel Formula Examples

### Progress Calculation
```excel
=IF(Status="Completed", 100, 
  IF(Status="In Progress", 
    ESTIMATED_PROGRESS_VALUE, 0))
```

### Days Remaining
```excel
=IF(Status="Completed", "Completed", 
  IF(Status="Planned", "Not Started", 
    TEXT(Target_Date-TODAY(), "0") & " days"))
```

### Conditional Formatting
- Green: Completed certifications
- Blue: In progress (>50% estimated)
- Orange: In progress (<50% estimated)
- Gray: Planned/not started
