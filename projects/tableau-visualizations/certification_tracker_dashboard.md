# Certification Tracker Visualization in Tableau

## Overview
Since you completed Tableau Desktop Specialist in January 2021, let's leverage those skills to create an interactive certification dashboard.

## Step 1: Prepare Data for Tableau

### Create CSV File
Save this data as `certification_tracker.csv`:

```csv
Certification,Platform,Status,Target_Date,Progress_Percent,Category,Priority
Google Data Analytics Professional,Coursera,In Progress,2025-03-01,75,Analytics,High
Microsoft Power BI Data Analyst Professional,Coursera,In Progress,2025-10-01,40,Analytics,High
Azure Data Engineer Associate,Microsoft Learn,Planned,2025-05-01,0,Engineering,Medium
Python for Data Science,Coursera,Planned,2025-04-01,0,Programming,High
Tableau Desktop Specialist,Tableau,Completed,2021-01-01,100,Visualization,Completed
dbt Fundamentals,dbt Labs,Planned,2025-11-01,0,Engineering,Medium
```

## Step 2: Tableau Worksheet Ideas

### Worksheet 1: Progress Bar Chart
- **Chart Type:** Horizontal Bar Chart
- **Rows:** Certification (sorted by Progress_Percent descending)
- **Columns:** Progress_Percent
- **Color:** Status (use traffic light colors)
- **Label:** Progress_Percent
- **Filter:** Exclude completed certifications if desired

### Worksheet 2: Timeline Gantt Chart
- **Chart Type:** Gantt Chart
- **Rows:** Certification
- **Columns:** Target_Date
- **Color:** Status
- **Size:** Progress_Percent
- **Detail:** Add tooltip with days remaining

### Worksheet 3: Status Summary
- **Chart Type:** Pie Chart or Donut Chart
- **Angle:** Number of Records
- **Color:** Status
- **Label:** Percentage and count

### Worksheet 4: Platform Analysis
- **Chart Type:** Tree Map
- **Size:** Number of Records
- **Color:** Average Progress_Percent
- **Detail:** Platform

### Worksheet 5: Category Breakdown
- **Chart Type:** Stacked Bar Chart
- **Rows:** Category
- **Columns:** Number of Records
- **Color:** Status

## Step 3: Create Interactive Dashboard

### Dashboard Layout
```
+------------------------------------------+
|           CERTIFICATION DASHBOARD        |
|              Kevin Spittler MBA          |
+------------------------------------------+
| Progress Chart          | Status Summary |
| (Main View)            | (Pie Chart)    |
|                        |                |
+------------------------+----------------+
| Timeline Gantt         | Platform       |
| (Interactive)          | Analysis       |
+------------------------+----------------+
| Summary Statistics     | Filters        |
+------------------------------------------+
```

### Interactive Elements
1. **Filter by Status:** Allow filtering by Completed/In Progress/Planned
2. **Filter by Category:** Analytics, Engineering, Programming, Visualization
3. **Date Range Filter:** Target completion dates
4. **Highlight Actions:** Click on status to highlight across all charts

### Calculated Fields

#### Days Remaining
```
IF [Status] = "Completed" THEN 0
ELSE DATEDIFF('day', TODAY(), [Target_Date])
END
```

#### Progress Status
```
IF [Progress_Percent] = 100 THEN "Completed"
ELSEIF [Progress_Percent] >= 50 THEN "On Track"
ELSEIF [Progress_Percent] > 0 THEN "Behind Schedule"
ELSE "Not Started"
END
```

#### Completion Quarter
```
"Q" + STR(DATEPART('quarter', [Target_Date])) + " " + STR(YEAR([Target_Date]))
```

## Step 4: Design and Formatting

### Color Scheme (Your Brand Colors)
- **Completed:** #4CAF50 (Green)
- **In Progress:** #FF9800 (Orange) 
- **Planned:** #2196F3 (Blue)

### Typography
- **Title:** Tableau Bold, 16pt
- **Subtitles:** Tableau Regular, 12pt
- **Labels:** Tableau Regular, 10pt

### Dashboard Actions
1. **Filter Action:** Click on status to filter all charts
2. **Highlight Action:** Hover to highlight related items
3. **URL Action:** Link to certification websites

## Step 5: Advanced Features

### Parameter Controls
- **View Type:** Switch between different chart types
- **Time Period:** Show current year, next year, or all
- **Sort Order:** By progress, alphabetical, or by target date

### Tooltip Enhancements
```
Certification: <Certification>
Platform: <Platform>
Current Progress: <Progress_Percent>%
Target Date: <Target_Date>
Days Remaining: <Days Remaining>
Category: <Category>
```

### Mobile Optimization
- Create mobile-friendly layout
- Simplify charts for smaller screens
- Ensure touch-friendly interactions

## Step 6: Publishing and Sharing

### Tableau Public
1. Publish to Tableau Public for portfolio
2. Create story points explaining your certification journey
3. Add to your LinkedIn profile and portfolio website

### Story Points
1. **Slide 1:** Overview of certification strategy
2. **Slide 2:** Current progress and achievements
3. **Slide 3:** Timeline and upcoming goals
4. **Slide 4:** Skills development roadmap

## Tableau Best Practices Applied

### Performance Optimization
- Use extracts for better performance
- Minimize calculated fields in views
- Optimize filters and parameters

### User Experience
- Clear navigation and intuitive design
- Consistent color scheme and formatting
- Responsive design for different devices

### Professional Presentation
- Clean, uncluttered layout
- Professional color scheme
- Clear titles and labels
- Appropriate chart types for data

---

## Portfolio Integration

This Tableau dashboard can be:
1. **Embedded in your portfolio website**
2. **Shared on LinkedIn as a professional update**
3. **Used in job interviews to demonstrate Tableau skills**
4. **Updated regularly to show ongoing progress**

The dashboard demonstrates both your Tableau technical skills and your strategic approach to professional development - perfect for your healthcare analytics career goals.
