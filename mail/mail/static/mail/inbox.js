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
  document.querySelector('#view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#email').value = '';
  document.querySelector('#subject').value = '';
  document.querySelector('#body').value = '';

  // Listening for an submition
  document.querySelector('form').onsubmit = send_email;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
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
  const view = document.querySelector('#view');
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  // .then(result => {
  //   console.log(result)
  // });
  .then(emails => {

    // The container holding all the emails
    const container = document.createElement('div');
    // container.style.border = "1px black solid";

    // The top divs that will hold the column names
    const div_top = document.createElement('div');
    const div_from_title = document.createElement('div');
    const div_sub_title = document.createElement('div');
    const div_time_title = document.createElement('div');
    
    div_top.style.display = "flex";
    div_from_title.order = "1";
    div_from_title.style.flexGrow = "2";
    div_from_title.style.paddingLeft = "10px";
    div_sub_title.order = "2";
    div_sub_title.style.flexGrow = "2";
    div_sub_title.style.paddingLeft = "10px";
    div_time_title.order = "3";
    div_time_title.style.flexGrow = "2";
    div_time_title.style.paddingLeft = "10px";

    // The names of the columns
    div_from_title.innerHTML = "From";
    div_sub_title.innerHTML = "Subject";
    div_time_title.innerHTML = "Received";

    // Adding the names to the top row div
    div_top.append(div_from_title);
    div_top.append(div_sub_title);
    div_top.append(div_time_title);

    // Top row added to the top of the container
    container.append(div_top);

    for(var i = 0; i < emails.length; i++) {

      // Getting each emails
      var obj = emails[i];

      // Container other than the top row
      const div_container = document.createElement('div');
      div_container.style.borderLeft = "2px black solid";
      div_container.style.borderRight = "2px black solid";
      
      if (i === 0) {
        div_container.style.borderTop = "2px black solid";
      } else {
        div_container.style.borderTop = "1px black solid";
      }
      if (i === (emails.length - 1)) {
        div_container.style.borderBottom = "2px black solid";
      } else {
        div_container.style.borderBottom = "1px black solid";
      }
      div_container.style.display = "flex";

      // Sender, Subject, and Time divs
      const div_sender = document.createElement('div');
      const div_subject = document.createElement('div');
      const div_time = document.createElement('div');

      // Making the whole div a link
      const email_link = document.createElement('a');

      // Padding, Flex, and other CSS modifiers.
      div_sender.innerHTML = obj.sender;
      div_sender.style.order = "1";
      div_sender.style.paddingLeft = "10px";

      div_subject.innerHTML = obj.subject;
      div_subject.style.order = "2";
      div_subject.style.paddingLeft = "10px";

      div_time.innerHTML = obj.timestamp;
      div_time.style.order = "3";
      div_time.style.paddingLeft = "10px";

      // Adding into the container as a whole
      div_container.append(div_sender);
      div_container.append(div_subject);
      div_container.append(div_time);

      // Sending the row container to the main container
      email_link.append(div_container);
      container.append(email_link);
    };

    // Added to the whole
    view.append(container);
  });
}