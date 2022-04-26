document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#mailbox').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#email').value = '';
  document.querySelector('#subject').value = '';
  document.querySelector('#body').value = '';

  // Listening for an submition
  document.querySelector('form').onsubmit = send_email;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#mailbox').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#mailbox').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  mb(mailbox);
}

function send_email() {
  const email = document.querySelector('#email').value;
  const subject = document.querySelector('#subject').value;
  const body = document.querySelector('#body').value;
  
  fetch('emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: email,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json());
  // .then(result => {
  //   console.log(result)
  // });
}

function mb(mailbox) {
  const view = document.querySelector('#mailbox');
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  // .then(result => {
  //   console.log(result)
  // });
  .then(emails => {

    // The container holding all the emails
    const container = document.createElement('div');
    container.style.display = "table";
    container.style.width = "100%";

    const table = document.createElement('table');
    table.style.borderCollapse = "collapse";
    table.style.width = "100%";

    const thead = document.createElement('thead');
    const thead_tr = document.createElement('tr');

    const sender_td = document.createElement('td');
    const subject_td = document.createElement('td');
    const time_td = document.createElement('td');
    subject_td.style.textAlign = "center";
    time_td.style.textAlign = "right";

    sender_td.innerHTML = "From";
    subject_td.innerHTML = "Subject";
    time_td.innerHTML = "Received";

    sender_td.style.fontWeight = 'bold';
    subject_td.style.fontWeight = 'bold';
    time_td.style.fontWeight = 'bold';

    thead_tr.appendChild(sender_td);
    thead_tr.appendChild(subject_td);
    thead_tr.appendChild(time_td);

    thead.appendChild(thead_tr);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');

    for(var i = 0; i < emails.length; i++) {

      // Getting each emails
      var obj = emails[i];

      let email_tr = document.createElement('tr');
      let sender = document.createElement('td');
      let subject = document.createElement('td');
      let time = document.createElement('td');

      subject.style.textAlign = "center";
      time.style.textAlign = "right";

      sender.innerHTML = obj.sender;
      subject.innerHTML = obj.subject;
      time.innerHTML = obj.timestamp;

      email_tr.appendChild(sender);
      email_tr.appendChild(subject);
      email_tr.appendChild(time);

      email_tr.style.border = "1px solid #888888";
      email_tr.onclick = function () {
        view_email(obj.id);
      };

      if (obj.read === true) {
        email_tr.style.backgroundColor = "#dddddd";
      }
      tbody.appendChild(email_tr);
    };

    table.appendChild(tbody);

    container.append(table)
    // Added to the whole
    view.append(container);
  });
}

function view_email(id) {

  // Show the mailbox and hide other views
  document.querySelector('#mailbox').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email').style.display = 'block';

  const view = document.querySelector('#email');

  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // console.log(email);
      const non_body = document.createElement("div");
      const div_body = document.createElement("div");
      const buttons = document.createElement("div");
      const from_header = document.createElement('p');
      const to_header = document.createElement('p');
      const subject = document.createElement('p');
      const time = document.createElement('p');
      const reply = document.createElement('button');
      reply.setAttribute("class", "btn btn-sm btn-outline-primary");
      reply.innerHTML = "Reply";
      buttons.append(reply);
      if (email.recipients.length > 1) {
        for (var i = 0; i < email.recipients.length; i++) {
          const replyall = document.createElement('button');
          replyall.innerHTML = "Reply all";
          replyall.setAttribute("class", "btn btn-sm btn-outline-primary");
          buttons.append(replyall);
          // do something with commas in between
          to_header.innerHTML = `<b>To: </b> ${email.recipients}`;
        };
      } else {
        to_header.innerHTML = `<b>To: </b> ${email.recipients}`;
      }
      const b = document.createElement('hr');

      const body = document.createElement('p');

      from_header.innerHTML = `<b>From: </b> ${email.sender}`;
      subject.innerHTML = `<b>Subject: </b> ${email.subject}`;
      time.innerHTML = `<b>Time: </b> ${email.timestamp}`;
      
      body.innerHTML = email.body;
      div_body.append(body);

      non_body.append(from_header);
      non_body.append(to_header);
      non_body.append(subject);
      non_body.append(time);
      non_body.append(buttons);

      view.append(non_body);
      view.append(b);
      view.append(div_body);
    });
}