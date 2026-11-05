
"""Flask Stack Simulator starter: completed version."""

import secrets

# P1: Import Flask tools for templates, forms, redirects, sessions, and messages.
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)

# Import the completed Stack class.
from stack_model import Stack

app = Flask(__name__)

# P2: Set SECRET_KEY for session and flash messages.
app.secret_key = secrets.token_hex(16)

# This lesson uses short fictional stack values on localhost.


@app.route('/')
def index():
    # P3: Display the simulator using the index.html template.

    # P6: Restore stack values from session, reverse for display,
    # and pass items, size, popped, and highlight to the template.
    stack = Stack(session.get('stack', []))
    popped = session.get('popped', [])
    highlight = session.get('highlight', False)

    # Display the top of the stack first.
    items = list(reversed(stack.items))

    return render_template(
        'index.html',
        items=items,
        size=stack.size(),
        popped=popped,
        highlight=highlight
    )


@app.route('/stack', methods=['POST'])
def operate():
    # P4: Read action and value from request.form. Strip the value.
    action = request.form.get('action', '').lower()
    value = request.form.get('value', '').strip()

    # P7: Restore the Stack and removed-item history from session.
    stack = Stack(session.get('stack', []))
    popped = session.get('popped', [])
    highlight = False

    # P8: Implement Push, Pop, Peek, and Clear with feedback.
    if action == 'push':
        # Push accepts 1-24 characters and at most 20 current items.
        if not value:
            flash('Please enter a value.', 'warning')
        elif len(value) > 24:
            flash('Value must be 24 characters or less.', 'warning')
        elif stack.size() >= 20:
            flash('The stack is full. Maximum is 20 items.', 'warning')
        else:
            stack.push(value)
            flash(f'{value} was pushed onto the stack.', 'success')

    elif action == 'pop':
        # Pop removes the top item and handles an empty stack.
        removed = stack.pop()

        if removed is None:
            flash('Cannot Pop: the stack is empty.', 'warning')
        else:
            popped.append(removed)

            # Keep only the 20 most recently removed values.
            popped = popped[-20:]
            flash(f'{removed} was removed from the stack.', 'success')

    elif action == 'peek':
        # Peek highlights the top item without removing it.
        if stack.is_empty():
            flash('Cannot Peek: the stack is empty.', 'warning')
        else:
            highlight = True
            flash(f'Top item is {stack.peek()}.', 'info')

    elif action == 'clear':
        # Clear resets both the stack and removed-item history.
        stack.clear()
        popped = []
        flash('Stack and removed items have been cleared.', 'info')

    else:
        flash('Invalid operation.', 'danger')

    # P9: Reassign session values, then redirect to the index route.
    # Use a peek flag when highlighting the top item.
    session['stack'] = stack.items
    session['popped'] = popped
    session['highlight'] = highlight

    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    # P5: Render contact.html as a placeholder landing page.
    return render_template('contact.html')


if __name__ == '__main__':
    # Local development only. Stop with Ctrl+C.
    app.run(debug=True)
