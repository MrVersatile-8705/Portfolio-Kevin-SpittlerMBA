# Certification Tracker in Power BI

## Overview
Perfect opportunity to practice your Power BI skills from the Data Analyst Professional Certificate course!

## Step 1: Data Preparation in Excel (Applying Your New Skills)

### Enhanced Data Model
```excel
Certifications Table:
ID | Certification | Platform | Status | Target_Date | Progress_Percent | Category | Priority | Cost | Duration_Weeks

1 | Google Data Analytics Professional | Coursera | In Progress | 2025-03-01 | 75 | Analytics | High | $49/month | 24
2 | Microsoft Power BI Data Analyst Professional | Coursera | In Progress | 2025-10-01 | 40 | Analytics | High | $49/month | 20
3 | Azure Data Engineer Associate | Microsoft Learn | Planned | 2025-05-01 | 0 | Engineering | Medium | Free | 12
4 | Python for Data Science | Coursera | Planned | 2025-04-01 | 0 | Programming | High | $49/month | 16
5 | Tableau Desktop Specialist | Tableau | Completed | 2021-01-01 | 100 | Visualization | Completed | Free | 8
6 | dbt Fundamentals | dbt Labs | Planned | 2025-11-01 | 0 | Engineering | Medium | Free | 6
```

### Additional Tables for Advanced Analytics

#### Skills_Mapping Table:
```excel
Certification_ID | Skill | Skill_Category | Industry_Relevance
1 | Data Cleaning | Technical | Healthcare Analytics
1 | Statistical Analysis | Technical | Healthcare Analytics
2 | DAX | Technical | Business Intelligence
2 | Data Modeling | Technical | Business Intelligence
```

#### Timeline_Tracking Table:
```excel
Certification_ID | Date | Progress_Percent | Notes
1 | 2024-09-01 | 25 | Started course
1 | 2024-10-01 | 50 | Completed first half
1 | 2024-11-01 | 75 | Current progress
```

## Step 2: Power BI Data Model Design

### Relationships
- **Certifications** (1) → (*) **Skills_Mapping** on Certification_ID
- **Certifications** (1) → (*) **Timeline_Tracking** on Certification_ID

### Calculated Columns

#### Days Remaining
```DAX
Days Remaining = 
IF(
    Certifications[Status] = "Completed",
    0,
    DATEDIFF(TODAY(), Certifications[Target_Date], DAY)
)
```

#### Progress Status
```DAX
Progress Status = 
SWITCH(
    TRUE(),
    Certifications[Progress_Percent] = 100, "Completed",
    Certifications[Progress_Percent] >= 50, "On Track",
    Certifications[Progress_Percent] > 0, "Behind Schedule",
    "Not Started"
)
```

#### Completion Quarter
```DAX
Target Quarter = 
"Q" & FORMAT(Certifications[Target_Date], "q") & " " & YEAR(Certifications[Target_Date])
```

### Measures

#### Total Investment
```DAX
Total Investment = 
SUMX(
    FILTER(Certifications, Certifications[Cost] <> "Free"),
    CURRENCY(LEFT(Certifications[Cost], FIND("/", Certifications[Cost]) - 1)) * 
    Certifications[Duration_Weeks] / 4
)
```

#### Average Progress
```DAX
Average Progress = 
AVERAGE(Certifications[Progress_Percent])
```

#### Completion Rate
```DAX
Completion Rate = 
DIVIDE(
    COUNTROWS(FILTER(Certifications, Certifications[Status] = "Completed")),
    COUNTROWS(Certifications)
) * 100
```

#### Skills Count
```DAX
Total Skills = 
DISTINCTCOUNT(Skills_Mapping[Skill])
```

## Step 3: Report Pages Design

### Page 1: Executive Overview
**Layout:** 
- Large KPI cards at top
- Progress chart in center
- Status distribution on right

**Visuals:**
1. **KPI Cards:**
   - Total Certifications
   - Completion Rate
   - Average Progress
   - Total Investment

2. **Main Chart:** Horizontal bar chart of progress by certification
3. **Donut Chart:** Status distribution
4. **Timeline:** Target completion dates

### Page 2: Detailed Analysis
**Visuals:**
1. **Matrix:** Detailed certification information
2. **Scatter Plot:** Progress vs. Days Remaining
3. **Stacked Column:** Certifications by category and status
4. **Line Chart:** Progress over time (using Timeline_Tracking)

### Page 3: Skills Development
**Visuals:**
1. **Tree Map:** Skills by category
2. **Clustered Bar:** Skills count by certification
3. **Word Cloud:** Industry-relevant skills
4. **Waterfall:** Skills progression timeline

### Page 4: Mobile View
**Optimized for mobile:**
- Simplified KPIs
- Single-column layout
- Touch-friendly filters

## Step 4: Advanced Features

### Bookmarks and Navigation
- **Status Filter:** Quick filter by completion status
- **Category View:** Switch between skill categories
- **Timeline View:** Different time period perspectives

### Drill-Through Pages
- **Certification Details:** Drill through to detailed certification info
- **Skills Analysis:** Drill through to skills breakdown

### Row-Level Security (RLS)
```DAX
[Platform] = USERNAME()
```
(For multi-user scenarios where different platforms might have restricted access)

## Step 5: Interactive Elements

### Slicers and Filters
- **Date Range:** Target completion dates
- **Platform:** Filter by learning platform
- **Category:** Analytics, Engineering, Programming, etc.
- **Status:** Completed, In Progress, Planned

### Cross-Filter Interactions
- Click on platform to highlight related certifications
- Select category to filter skills view
- Hover over progress chart to show detailed tooltip

### Custom Tooltips
Create custom tooltip page showing:
- Certification details
- Skills gained
- Progress timeline
- Industry relevance

## Step 6: Professional Formatting

### Theme and Colors
Create custom theme with your brand colors:
```json
{
    "name": "Kevin Spittler Portfolio Theme",
    "dataColors": ["#2E86AB", "#F26419", "#F6F5F5", "#A23B72", "#F18F01"],
    "background": "#FFFFFF",
    "foreground": "#333333"
}
```

### Typography
- **Headers:** Segoe UI Bold
- **Body Text:** Segoe UI Regular
- **Numbers:** Segoe UI Semibold

## Step 7: Publishing and Sharing

### Power BI Service
1. Publish to Power BI Service
2. Create app for external sharing
3. Schedule data refresh (if using live data)
4. Set up alerts for milestone achievements

### Embedded Options
- Embed in portfolio website
- Share link on LinkedIn
- Include in job application portfolios

## Step 8: Portfolio Integration

### Documentation
Create accompanying documentation:
- Design rationale
- DAX formulas explanation
- Business insights generated
- Technical skills demonstrated

### LinkedIn Content
- "How I Visualized My Professional Development Journey in Power BI"
- Technical tips and DAX formulas used
- Business value of tracking certifications

### Interview Preparation
Use this dashboard to demonstrate:
- Power BI technical skills
- Self-directed learning approach
- Strategic career planning
- Data-driven decision making

---

## Learning Outcomes

This Power BI project demonstrates:
1. **Data modeling best practices**
2. **Advanced DAX calculations**
3. **Professional dashboard design**
4. **Mobile optimization**
5. **Business storytelling with data**

Perfect example of applying your Power BI Data Analyst Professional Certificate skills to personal career development!
