# Your First MUSHcode

## What Is MUSHcode?

MUSHcode (also called softcode) is the programming language built into every
MUSH server. It lets you create interactive objects, automated systems, and
custom commands. Everything from a simple greeting robot to a full combat
system can be built with MUSHcode.

MUSHcode is different from most programming languages you may have seen. It
is evaluated inline, embedded in object attributes, and uses a functional
style where everything is a function call. There are no statements, no
semicolons, and no separate source files. Your code lives on objects in the
game.

## The think Command: Your Playground

The `think` command evaluates an expression and shows you the result. It is
the best way to experiment:

```
> think Hello, World!
Hello, World!
```

That was plain text. Now let's call a function:

```
> think add(2, 3)
5
```

The `add()` function adds numbers. Functions are called with parentheses and
comma-separated arguments, just like in math or most programming languages.

```
> think mul(4, 5)
20
> think strlen(Hello)
5
> think ucstr(hello world)
HELLO WORLD
```

## Square Brackets: Evaluation

In MUSHcode, square brackets `[]` tell the evaluator to evaluate their
contents as an expression. Outside of `think`, you need them:

```
> say The answer is [add(2, 3)].
You say, "The answer is 5."
```

Without brackets, the function would not be evaluated:

```
> say The answer is add(2, 3).
You say, "The answer is add(2, 3)."
```

Inside `think`, everything is already evaluated, so brackets are optional.
But in attributes, messages, and commands, brackets are essential.

## Percent Codes: Substitution

Percent codes are special tokens that the evaluator replaces with values.
The most common ones:

| Code | Meaning |
|------|---------|
| `%#` | The dbref of the player who triggered the action. |
| `%!` | The dbref of the object running the code. |
| `%n` | The name of the triggering player. |
| `%l` | The dbref of the triggering player's location. |
| `%r` | A newline (carriage return). |
| `%b` | A space (blank). |
| `%t` | A tab character. |

Try them:

```
> think My dbref is %#
My dbref is #42
> think My name is %n
My name is Sparrow
> think I am in room %l
I am in room #5
```

## Your First Interactive Object

Let's create an object that responds when you use it:

```
> @create Greeter
Greeter created as object #400.
> @desc Greeter = A small brass automaton with a friendly face.
> &CMD_GREET Greeter = $greet:@pemit %# = The Greeter waves
  and says, "Hello, [name(%#)]! Welcome!"
```

Now try it:

```
> greet
The Greeter waves and says, "Hello, Sparrow! Welcome!"
```

Let's break down the code:

- `&CMD_GREET Greeter` -- We are setting an attribute called CMD_GREET on
  the Greeter object.
- `$greet:` -- The `$` prefix defines a user command. When anyone in the
  room types `greet`, this code runs.
- `@pemit %#` -- Sends a private message to the player who typed the
  command.
- `[name(%#)]` -- Calls the `name()` function on the triggering player's
  dbref to get their name.

## Nesting Functions

Functions can be nested inside each other:

```
> think ucstr(left(Hello World, 5))
HELLO
```

The evaluator works from the inside out:

1. `left(Hello World, 5)` returns `Hello`.
2. `ucstr(Hello)` returns `HELLO`.

You can nest as deeply as you need:

```
> think add(mul(3, 4), sub(10, 5))
17
```

This computes `(3 * 4) + (10 - 5) = 12 + 5 = 17`.

## Braces: Grouping

Curly braces `{}` group text that contains commas or other special
characters. Without braces, commas separate function arguments. The
`first()` function takes a list as its first argument and returns the
first element:

```
> think first(apple banana cherry)
apple
```

With braces, commas are protected from being treated as argument
separators:

```
> think first({apple, banana, cherry})
apple,
```

Without braces, `first(apple, banana, cherry)` passes three separate
arguments to a function that expects at most two (list and delimiter).
Braces are essential when passing complex text to functions. You will use
them constantly.

## Action Lists

An action list is a sequence of commands separated by semicolons. They
run one after another:

```
> &CMD_ROLL Greeter = $roll:@pemit %# = You roll the dice...;
  @pemit %# = You got [die(2, 6)]!
```

```
> roll
You roll the dice...
You got 8!
```

Each command in the action list is a separate game command (`@pemit`,
`say`, `@emit`, etc.). The semicolons separate them.

## Putting Code on Objects

All MUSHcode lives in attributes on objects. There are several patterns:

**\$-commands** respond to player input:

```
> &CMD_TIME me = $time:@pemit %# = The time is [time()].
```

**Action attributes** run when events occur:

```
> @asucc door = @pemit %# = The door creaks as you push it open.
```

**User functions** are called by other code:

```
> &FN_DOUBLE me = mul(%0, 2)
> think u(me/FN_DOUBLE, 21)
42
```

## Common Beginner Mistakes

**Forgetting square brackets:**

```
> say It is add(1,1) o'clock.     <-- Wrong
You say, "It is add(1,1) o'clock."

> say It is [add(1,1)] o'clock.   <-- Right
You say, "It is 2 o'clock."
```

**Commas inside function arguments:**

```
> @pemit %# = Hello, how are you?  <-- Comma may confuse things
> @pemit %# = {Hello, how are you?}  <-- Braces protect the comma
```

**Missing the \$ in commands:**

```
> &CMD me = greet:say Hi           <-- Missing $
> &CMD me = $greet:say Hi          <-- Correct
```

## Experimenting

The best way to learn MUSHcode is to experiment. Use `think` to test
expressions. Create test objects and try things on them. Break things
deliberately to see what happens. There is no way to damage the game by
experimenting on your own objects.

```
> think cat(Hello, World)
Hello World
> think strcat(Hello, World)
HelloWorld
> think capstr(hello)
Hello
> think reverse(Hello)
olleH
```

In the next chapters, you will learn about variables, control flow, string
manipulation, lists, and how to build real systems.
