# *mesme*

## What is *mesme*?

*mesme* is a tool for time tracking. It is designed to log the time that is spent on tasks.

## Concept

### Users

There can be multiple users on a single machine, although not simultaneously. When *mesme* is started, the user can
login with his account or create a new account. An account consists of a name.

In *mesme*, the user can only see tasks and tracking data for his own account.

### Tasks

The user can create tasks (title / description) and bring them into a custom order.
The user can select a task and start tracking time for that task.
*mesme* logs how much time is spent on each task.

An item can have different states: *Backlog* / *In progress* / *Done*

There is a special task *General work*. This task does not have a state and can always be selected. It is not visible in
the table view. After the *General work* task was selected, the user can enter a description. Once the tracking for that
task stops, the time is logged with the entered description.

### Table view (unfinished tasks)

In the table view all unfinished tasks are listed as items. The item shows the state of the task and how much time is
already logged.

Each item has buttons: *Start* / *Edit* / *Delete*.
* When *Start* is pressed, that task will be selected (meaning that the tracked time is now logged for this task).
* When *Edit* is pressed, title / description can be changed. Also the tracked time can be moved to another task (if the
  user forgot to select a new task).
* When *Delete* is pressed, the task is deleted. *(Move already tracked time to another task?)*

### Global states

There user can be in different (global) states: *At work* / *Pause* / *At home*

When the user starts tracking time, the global state switches to *At work*. When the user presses the pause button, the
global state switches to *Pause* and the time tracking for tasks stops. Instead, the pause time is tracked. When the
user presses the work-done button, the global state switches to *At home* and no time is tracked at all.
