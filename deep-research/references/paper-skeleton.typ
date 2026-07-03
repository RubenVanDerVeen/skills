// Paper skeleton for the research profile.
// Load typst-pro before using this. Adjust to your venue.
// Run with: typst compile main.typ

#import "@local/typst-tools/lib.typ": *

#show: project.with(
  title: "<TITLE>",
  author: "<AUTHOR>",
  course: "<COURSE_OR_VENUE>",
  date: datetime.today(),
)

= Introduction

<from dossier TL;DR + claim 1>

= Background

<what the reader needs to know>

= Related Work

<from dossier State of the Art>

= Methodology / Approach

<from dossier claims 4-7>

= Results / Discussion

<from dossier claims 8+>

= Open Problems

<from dossier Open Questions & Gaps>

= Conclusion

<one-sentence contribution + future work>

= References

// Use typst-pro's bibliography helper. For arxiv-only papers, manual list is fine.
