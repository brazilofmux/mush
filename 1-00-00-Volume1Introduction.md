# Introduction to The MUSH Standard

For over thirty years, MUSH servers have provided a unique form of online
interaction: a programmable, text-based virtual world where users build rooms,
create objects, and write code that brings their creations to life. From
role-playing communities to educational environments, from social gathering
places to experimental programming platforms, MUSH servers have served an
extraordinary range of purposes -- all built on a common technical foundation
that has never been formally documented.

This volume is that document.

The MUSH Standard specifies what a MUSH server is, precisely and completely.
It defines the object model that structures the virtual world, the command
language that lets users interact with it, the expression evaluator that powers
MUSHcode programming, and the systems -- channels, mail, locks, permissions --
that make a MUSH a living, shared environment. If you implement the behaviors
described in this book, you will have built a MUSH server. If you write softcode
that relies only on the behaviors described in this book, your code will run on
any conforming server.

This standard draws on four major implementations that have evolved over three
decades: TinyMUSH, TinyMUX, RhostMUSH, and PennMUSH. Each has its strengths,
its extensions, its particular community of users and developers. Where they
agree -- and they agree far more often than they disagree -- this standard
codifies their shared behavior. Where they diverge, this standard makes
explicit choices, identifies optional features, and marks implementation-defined
behavior so that both implementors and users know exactly where they stand.

Two of these implementations, TinyMUSH and TinyMUX, have agreed to implement
this standard. The goal is not to constrain creativity or freeze the
technology, but to establish a common baseline that enables portability,
interoperability, and a shared vocabulary for the MUSH community going forward.

This standard is organized into nine parts. Part I establishes scope,
conformance, and notation. Parts II through IV define the core of the system:
the object model, command processing, and the evaluation engine. Parts V and
VI catalog the built-in commands and functions. Part VII addresses security and
permissions. Part VIII covers the communication and persistence systems. Part
IX defines conformance levels and documents the boundary between standard and
extension.

Read sequentially, this standard takes you from first principles to a complete
specification of a MUSH server. Read as a reference, it provides definitive
answers to questions about how a conforming implementation shall behave.

The companion volume, *The MUSH User's Manual*, approaches the same technology
from the other direction: not "how should it work?" but "how do I use it?"
Together, the two volumes provide a complete picture of MUSH technology for
implementors, administrators, and users alike.
