
"""Flask Queue Simulator: First In, First Out (FIFO)."""

import secrets

# P1: Import Flask tools for templates, forms, redirects, sessions, and messages.
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)

# Import the Queue class.
from queue_model import Queue

app = Flask(__name__)

# P2: Set SECRET_KEY for session and flash messages.
app.secret_key = secrets.token_hex(16)

# This lesson uses short fictional queue values on localhost.


@app.route('/')
def index():
    # P3: Display the simulator using the index.html template.

    # P6: Restore queue values from session.
    # Queue items are displayed from Front to Rear.
    queue = Queue(session.get('queue', []))
    removed = session.get('removed', [])
    highlight = session.get('highlight', False)

    items = queue.items

    return render_template(
        'index.html',
        items=items,
        size=queue.size(),
        removed=removed,
        highlight=highlight
    )


@app.route('/queue', methods=['POST'])
def operate():
    # P4: Read action and value from request.form. Strip the value.
    action = request.form.get('action', '').lower()
    value = request.form.get('value', '').strip()

    # P7: Restore the Queue and removed-item history from session.
    queue = Queue(session.get('queue', []))
    removed = session.get('removed', [])
    highlight = False

    # P8: Implement Enqueue, Dequeue, Peek, and Clear with feedback.
    if action == 'enqueue':
        # Enqueue accepts 1-24 characters and at most 20 current items.
        if not value:
            flash('Please enter a value.', 'warning')
        elif len(value) > 24:
            flash('Value must be 24 characters or less.', 'warning')
        elif queue.size() >= 20:
            flash('The queue is full. Maximum is 20 items.', 'warning')
        else:
            queue.enqueue(value)
            flash(f'{value} was added to the rear of the queue.', 'success')

    elif action == 'dequeue':
        # Dequeue removes the front item and handles an empty queue.
        item = queue.dequeue()

        if item is None:
            flash('Cannot Dequeue: the queue is empty.', 'warning')
        else:
            removed.append(item)

            # Keep only the 20 most recently removed values.
            removed = removed[-20:]
            flash(f'{item} was removed from the front of the queue.', 'success')

    elif action == 'peek':
        # Peek highlights the front item without removing it.
        if queue.is_empty():
            flash('Cannot Peek: the queue is empty.', 'warning')
        else:
            highlight = True
            flash(f'Front item is {queue.peek()}.', 'info')

    elif action == 'clear':
        # Clear resets both the queue and removed-item history.
        queue.clear()
        removed = []
        flash('Queue and removed items have been cleared.', 'info')

    else:
        flash('Invalid operation.', 'danger')

    # P9: Reassign session values, then redirect to the index route.
    # Use a peek flag when highlighting the front item.
    session['queue'] = queue.items
    session['removed'] = removed
    session['highlight'] = highlight

    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    # P5: Render contact.html as a placeholder landing page.
    return render_template('contact.html')


if __name__ == '__main__':
    # Local development only. Stop with Ctrl+C.
    app.run(debug=True)
