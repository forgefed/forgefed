# Classes

## IssueTracker

An entity that can have a list of issues attached to it. It can be a
repository, or a project, anything that can have its own list of issues. Note
that while in repo hosting platforms issue are often attached to repos, this is
*not* always the case, and it doesn't have to be this way (for example projects
can use issue trackers where an issue can be associated with any number of
repos). This class abstracts that concept of something that gets a list of
issues attached.

Superclasses: None

## Issue

Superclasses: None

## User

Right now let's say it's someone or something that can do actions, in
particular open an issue. So it can be a real person, or it can be a bot. But
it probably shouldn't be a group. It's an individual, either real human or
automated software.

Superclasses: ActivityPub Actor?

# Properties

## next-issue-number

An issue tracker assigns numeric IDs to issues attached to it when they're
created. Issue IDs could also be UUIDs and things like that, in which case this
property is irrelevant of course.

Superproperties: None

Domain: IssueTracker

Range: Positive integer

## tracker

The issue tracker to which an issue belongs.

Superproperties: None

Domain: Issue

Range: IssueTracker

## issue-number

The numeric ID assigned to an issue by the tracker.

Superproperties: None

Domain: Issue

Range: Positive integer

## author

The user who created a given issue. However note that issues may be edited, so
this is NOT necessarily the user who's responsible for the current content of
the issue! It's just who *initially* created it. Maybe change "author" to
"creator" to be precise?

Superproperties: None

Domain: Issue

Range: User

## title

One-line description of an issue.

Superproperties: None

Domain: Issue

Range: Unicode text (one line though, i.e. no newlines)

## description

Detailed description of an issue.

Superproperties: None

Domain: Issue

Range: Media tagged text? I mean, one option is Markdown. Another is HTML with
some specific tags allowed. Another is text with a media type i.e. it can be
various content types, and whoever displays the issue on a computer screen
figures out the rendering details.

## creation-time

The time at which an issue was created.

Superproperties: None

Domain: Issue

Range: UTC time? Attach timezone to it?
