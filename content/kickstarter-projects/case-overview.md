# Kickstarter Projects Case Overview

[Kickstarter](https://www.kickstarter.com/) is a popular crowdfunding platform that allows creators to raise funds for their projects by soliciting contributions from a large number of people. The dataset we will be working with contains information about various Kickstarter projects, including their categories, funding goals, amounts pledged, and other relevant details.

The dataset has been provided by [webrobots.io](https://webrobots.io/kickstarter-datasets/) and contains information about projects launched on Kickstarter. The data is available in CSV format and includes various columns such as project ID, name, category, main category, currency, deadline, goal, pledged amount, state (e.g., successful, failed), backers count, and more.

While the dataset is rich in information, it may require some preprocessing to make it suitable for analysis. This may include tasks such as selecting relevant columns, filtering based on project state, checking the distribution of boolean columns, and converting epoch timestamps to datetime format for easier analysis.

Additionally, some columns may contain nested JSON information, such as the "video" column, which may require parsing to extract relevant details about the project's video content. Similarly, the "category" column may contain hierarchical information that can be parsed to analyze trends across different categories and subcategories of projects.

While parsing JSON columns is not a particularly difficult task, it can be time-consuming if you encounter malformed JSON data. Therefore, it is important to handle such cases gracefully, perhaps by using error handling techniques or alternative methods like regular expressions to extract relevant information without fully parsing the JSON.

We will begin by working with a small subset of the data. Then, we will work with the larger preprocessed dataset to perform various analyses and gain insights into the factors that contribute to the success or failure of Kickstarter projects.

## Questions to Answer

### Overall Success Rates

- What is the overall success rate?
- What is the mean and median pledged amount for successful vs failed projects?

### Category

- Which categories have the highest success rates?
- Which parent categories perform the best?
- Are some categories high funding but low success?

### Geography

- Which countries have the highest success rates?
- Does average pledged amount differ by country?
- Is the US materially different?

### Staff Pick & Spotlight

- What is the success rate for staff picks vs non-staff picks?
- What about spotlighted projects?

### Videos

- Do projects with videos have higher success rates?
- Do higher resolution videos correlate with higher success rates?
