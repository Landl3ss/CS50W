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
  document.querySelector('#to').value = '';
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
  let email = document.querySelector('#to').value;
  let subject = document.querySelector('#subject').value;
  let body = document.querySelector('#body').value;
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: email,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result)
    return false;
  });
}


function mb(mailbox) {
  let view = document.querySelector('#mailbox');
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // console.log(emails)
  // })
  // .then(email => {

    // The container holding all the emails
    let container = document.createElement('div');
    container.style.display = "table";
    container.style.width = "100%";

    let table = document.createElement('table');
    table.style.borderCollapse = "collapse";
    table.style.width = "100%";

    let thead = document.createElement('thead');
    let thead_tr = document.createElement('tr');

    let sender_td = document.createElement('td');
    let subject_td = document.createElement('td');
    let time_td = document.createElement('td');
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

    let tbody = document.createElement('tbody');

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
      email_tr.setAttribute("id", `${obj.id}`)

      email_tr.style.border = "1px solid #888888";
      // email_tr.onclick = function () {
      //   view_email(obj.id);
      // };

      if (obj.read === true) {
        email_tr.style.backgroundColor = "#dddddd";
      }
      tbody.appendChild(email_tr);
    };

    table.appendChild(tbody);

    container.append(table)
    // Added to the whole
    view.append(container);

    document.querySelectorAll("tr").forEach(row => row.onclick = function() {
      view_email(row.id);
    })
  });
}


function view_email(id) {

  // Show the mailbox and hide other views
  document.querySelector('#mailbox').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email').style.display = 'block';

  document.querySelector('#email').innerHTML = "";
  let view = document.querySelector('#email');


  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      console.log(email);
      let non_body = document.createElement("div");
      let div_body = document.createElement("div");
      let buttons = document.createElement("div");
      let from_header = document.createElement('p');
      let to_header = document.createElement('p');
      let subject = document.createElement('p');
      let time = document.createElement('p');
      let reply = document.createElement('button');
      let to_archive = document.createElement('button');
      if (email.archived === false) {
        to_archive.innerHTML = "Archive?";
      } else {
        to_archive.innerHTML = "Unarchive?";
      }
      to_archive.setAttribute("class", "btn btn-sm btn-outline-primary");
      reply.setAttribute("class", "btn btn-sm btn-outline-primary");
      reply.innerHTML = "Reply";
      reply.onclick = function () {
        reply_to(email);
      };
      to_archive.onclick = function () {
        archive_move(email);
      }
      // reply.style.margin = "20px";
      to_archive.style.marginLeft = "20px";
      buttons.append(reply);
      buttons.append(to_archive);
      if (email.recipients.length > 1) {
        let to_all = "";
        for (var i = 0; i < email.recipients.length; i++) {

          // do something with commas in between
          var rec = email[i];
          if (i != 0) {
            to_all += `, ${rec.recipients}`;
          } else {
            to_all += `${rec.recipients}`;
          }
        };
        to_header.innerHTML = `<b>To: </b> ${to_all}`;
      } else {
        to_header.innerHTML = `<b>To: </b> ${email.recipients}`;
      }
      let b = document.createElement('hr');

      let body = document.createElement('p');

      from_header.innerHTML = `<b>From: </b> ${email.sender}`;
      subject.innerHTML = `<b>Subject: </b> ${email.subject}`;
      time.innerHTML = `<b>Time: </b> ${email.timestamp}`;
      
      body.innerHTML = email.body;
      div_body.append(body);
      // div_body.append(body.innerHTML.replace(/\n/g, "</p><p>"));
      // console.log(body.innerHTML.replace(/\n/g, </p><p>));
      console.log(body.innerHTML);

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


function reply_to(email) {

  // Show compose view and hide other views
  document.querySelector('#mailbox').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#to').value = email.sender;
  if (email.subject.slice(0,4) === "Re: ") {
    document.querySelector('#subject').value = email.subject;
  } else {
    document.querySelector('#subject').value = `Re: ${email.subject}`;
  }
  document.querySelector('#body').value = `\n\nOn ${email.timestamp} ${email.sender} wrote: \n\n${email.body}`;

  // Listening for an submition
  document.querySelector('form').onsubmit = send_email;
}


function archive_move(email) {
  if (email.archived === true) {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
  } else {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  }
}