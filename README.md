# Netflix popularity

__What content on Netflix has the highest popularity?__

## Motivation

The purpose of this research is to gain insight into whether Netflix original,
exclusive and/or simultaneously released content is more popular compared to 
other content in the Netflix library. This popularity is measured by the amount and
valence of reviews. This project helps to understand the current dynamics of
creating popular content in the streaming video on demand market. Considering 
that acquiring popular, licensed content versus producing new titles can be highly
costly, this research clarifies whether such content strategy is fruitful in terms
of popularity. 

## Method

The data collected in this research is originated from IMDb and TMDb. These websites
provide an overview of content-specific information including the distributors involved,
producers involved, release dates and reviews written. These variables are needed in 
order to assess whether content is exclusive (Netflix is only distributor), original
(Netflix is one of the producers), simultaneously released (entire season is released
at once), whether the review has been written one week or after one week of release, and
how great the discrepancy is between release date and the review date. It is analyzed
what content strategy (original, exclusive, simultaneous release) reaps the greatest 
benefits in terms of popularity, and what the influence of time is on popularity of 
content.

## Results

### Descriptive statistics

According to our data, Netflix content library has been expanding since 2007 when it 
started to enter the streaming video-on-demand market. Specifically, the ratio of
exclusive content has been increasing from 0.357 in 2009 to 0.757 in 2020. Likewise,
Netflix has expanded its content library with originals, coming from a ratio of 0.0385
in 2011 to 0.105 in 2020. Striking to see is that release strategies of simultaenous 
releases have been increasing over the year, where in 2013 0.0578 of the content 
collected was simultaenously released, in 2020 this was 0.558. 

### Regression results 

Regarding the regression on volume of reviews and valence of review rating, it is found
that exclusive, original, simultaneous releasing has a positive effect on number of reviews.
Yet, this effect is highest for original shows. Moreover, it is found that for review rating
only original content has a positive effect. 

## Repository overview

\src\collection         <- collect data from imdb and tmdb\
\src\data-preparation   <- transform the raw data into usable variables for regression\
\src\analysis           <- regress the data

## Running instructions

### Collection

Needed: TMDB_API = {api_key} as environment variable. This API key can be obtained by creating
an account on TMDB and subsequentially an API. This variable is needed in order to gain
information on the release dates of all content. 

### Data preparation and analysis

Needed: GNUmake. The entire workflow is automated (except for the data collection). Hence, in order
to run this automated workflow. GNUmake can be installed from https://sourceforge.net/projects/gnuwin32/files/make/3.81/make-3.81.exe/download?use_mirror=jztkft&download=.
Installation instructions can be found on https://tilburgsciencehub.com/building-blocks/configure-your-computer/automation-and-workflows/make/

## About

This repository has been created by Bobbie and Sjors as part of a project at Tilburg University.
