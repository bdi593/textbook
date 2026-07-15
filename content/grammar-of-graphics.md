# Grammar of Graphics

The Grammar of Graphics provides a formal framework for describing and creating data visualizations. Think of it like the grammar of a language. Just as English grammar gives you rules to combine words (nouns, verbs, adjectives) into meaningful sentences, a Grammar of Graphics gives you "rules" to combine independent components into a meaningful plot.

The concept was most famously developed by Leland Wilkinson in his book, The [_Grammar of Graphics_](https://a.co/d/ak603Ld). The most popular implementation of this idea is the [`ggplot2`](https://ggplot2.tidyverse.org/) package in the R programming language, created by Hadley Wickham.

```{image} images/grammar-of-graphics/ggplot2-hex-logo.png
:alt: ggplot2 logo
:width: 240px
:align: center
```

:::{seealso} Leland Wilkinson's Influence

```{image} images/grammar-of-graphics/leland-wilkinson.jpg
:alt: Leland Wilkinson
:width: 240px
:align: left
```

Leland Wilkinson, the author of _The Grammar of Graphics_, was a statistician and computer scientist. His work laid the foundation for modern data visualization techniques. Wilkinson's ideas have influenced many visualization tools and libraries beyond ggplot2, including Python's plotnine, Tableau, and others.

In fact, he worked at SPSS (a major statistical software company) and contributed to the development of visualization features in SPSS.

Then, he joined Tableau where he worked on enhancing Tableau's visualization capabilities based on improving the theoretical and computational foundations of Tableau's visualization system.

He passed away in 2021, but his contributions continue to shape how we think about and create visualizations today.

:::

## Core Concepts

- Data: the dataset being visualized (usually a table, e.g., a data frame).
- Aesthetic mappings (aesthetics): how variables in the data are mapped to visual properties such as x, y, color, size, shape, alpha (transparency), etc.
- Geometric objects (geoms): the visual marks used to represent data (points, lines, bars, boxes, etc.).
- Statistical transformations (stats): computations that transform the data for plotting (e.g., binning, smoothing, summarizing). Some geoms apply a default stat.
- Scales: control how data values are translated into aesthetic values (e.g., color scales, continuous vs discrete scales, axis transforms).
- Coordinate system: Cartesian, polar, flipped coordinates, etc.
- Facets (small multiples): splitting data into subsets and drawing the same plot for each subset (faceting by one or more variables).
- Layers: plots are built by stacking layers (each layer typically specifies a geom and a mapping). Layers can have their own data/mappings/stats.
- Themes and annotations: control non-data ink like fonts, backgrounds, legend placement, and add annotations (text, lines, arrows).

## How ggplot2 and plotnine map the grammar

Both **ggplot2** (R) and **plotnine** (a Python port inspired by ggplot2) implement the grammar's ideas with a similar API. The mapping of concepts is straightforward:

- Data -> the data frame passed to ggplot()/ggplot(data=...) or plotnine's ggplot(data)
- Aesthetics -> aes() in ggplot2 and aes() in plotnine
- Geoms -> geom_point(), geom_line(), geom_bar(), etc. (same names in plotnine)
- Stats -> stat\_\* functions or `stat=` arguments on geoms
- Scales -> scale\_\* functions, e.g., scale_color_manual(), scale_x_log10()
- Facets -> facet_wrap(), facet_grid() (plotnine provides the same)
- Coordinate -> coord_flip(), coord_polar(), etc.
- Layers -> add geoms and stats with + in ggplot/plotnine
- Themes -> theme\_\*() and theme() customization

## Minimal examples

R / ggplot2 example:

```r
library(ggplot2)
ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
	geom_point(alpha = 0.7) +
	geom_smooth(method = "loess", se = FALSE) +
	facet_wrap(~ drv) +
	labs(title = "Engine displacement vs highway mpg",
			 x = "Displacement (L)", y = "Highway mpg") +
	theme_minimal()
```

Python / plotnine example:

```python
from plotnine import ggplot, aes, geom_point, geom_smooth, facet_wrap, labs, theme_minimal
from plotnine.data import mpg

(
		ggplot(mpg, aes('displ', 'hwy', color='class'))
		+ geom_point(alpha=0.7)
		+ geom_smooth(method='loess', se=False)
		+ facet_wrap('~drv')
		+ labs(title='Engine displacement vs highway mpg', x='Displacement (L)', y='Highway mpg')
		+ theme_minimal()
)
```

These examples show the principal pieces: a data source, aesthetic mappings, geoms (points and smooth lines), faceting, labels, and a theme.

## Layers, mappings, and overriding

One powerful feature is that layers can have their own data or aesthetics which override the plot-level defaults. For example, show raw points for all data but add a smoothed line for a filtered subset:

```r
ggplot(df, aes(x, y)) +
	geom_point() +
	geom_smooth(data = subset(df, group == 'A'), aes(x, y), method = 'lm')
```

Same idea in plotnine with the `data=` argument on a layer.

## Scales and transforms

Scales control how values map to aesthetics and how axes/legends are presented. Examples:

- Use `scale_y_log10()` to log-transform the y-axis while keeping the data unchanged (scale applies a transform for display).
- Use `scale_color_manual()` to set specific colors for factor levels.

Statistical transformations are also composable: `geom_bar()` by default uses `stat='count'` while `geom_col()` plots pre-computed heights.

## Faceting (small multiples)

Facets are a core grammar concept for conditioned plots. `facet_wrap(~ var)` creates a panel for each level of `var`. `facet_grid(row ~ col)` arranges panels in a grid based on two variables.

## Coordinate systems and theme

Coordinate systems (e.g., `coord_flip()` to swap x/y or `coord_polar()` for circular plots) are separate from geoms and scales, which makes it easier to change visual presentation without rewiring mappings.

Themes control non-data appearance: `theme_minimal()`, `theme_classic()`, and `theme()` for fine-grained control over text, grids, and backgrounds.

## Practical tips when using ggplot/plotnine

- Start by specifying the dataset and global aesthetics in `ggplot(data, aes(...))`.
- Add geoms as separate layers so you can mix different mark types and statistics.
- Use `aes()` for mappings that depend on the data. Set aesthetic values outside `aes()` for constant values (e.g., `color = 'red'` vs `aes(color=var)`).
- Prefer `geom_col()` when you already have counts/summaries, and `geom_bar()` when you want automatic counting.
- When debugging, print the plot object (in plotnine) or view the plot in an interactive environment to see how layers compose.

## Differences and notes between ggplot2 and plotnine

- Plotnine aims to mirror ggplot2's API, but not every extension or feature of ggplot2 is present. For R-specific packages (e.g., `ggthemes`, `patchwork`, `gganimate`), equivalents may differ or require different libraries in Python.
- Performance: ggplot2 is implemented in R and often benefits from R's ecosystem; plotnine is pure Python and integrates well with pandas workflows.
- Interactivity: ggplot2 produces static plots; interactive extensions (e.g., `plotly::ggplotly`) exist. Plotnine plots can be converted to interactive Plotly figures with `plotly` conversions but may require extra steps.

## Quick "Try it" (install and run)

- R (ggplot2):

```r
install.packages('ggplot2')
library(ggplot2)
# then run the example above
```

- Python (plotnine):

```bash
pip install plotnine mizani
```

Then run the Python example in a notebook or script.

## Further reading and resources

- L. Wilkinson, "The Grammar of Graphics" (book): the foundational text.
- Hadley Wickham, ggplot2 documentation: https://ggplot2.tidyverse.org
- Plotnine documentation: https://plotnine.readthedocs.io
- Tidyverse/ggplot2 cheatsheets and examples: https://www.rstudio.com/resources/cheatsheets/

---

This document provides a concise overview to help you reason about plots compositionally. When you move to building models and visualizing model outputs, the grammar helps you separate data transformation (stats) from presentation (scales, geoms, themes).
