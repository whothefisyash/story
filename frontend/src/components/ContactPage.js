import React from "react";
import "./ContactPage.css";

function ContactPage() {
  return (
    <div className="contact-page">
      <div className="contact-header">
        <h1>Contact Us</h1>
        <p>We would love to hear from you! Please fill out the form below to get in touch with us.</p>
      </div>
      <form className="contact-form">
        <label htmlFor="name">Name:</label>
        <input type="text" id="name" name="name" placeholder="Enter your name" required />

        <label htmlFor="email">Email:</label>
        <input type="email" id="email" name="email" placeholder="Enter your email address" required />

        <label htmlFor="message">Message:</label>
        <textarea id="message" name="message" rows="5" placeholder="Write your message here..." required></textarea>

        <button type="submit">Send Message</button>
      </form>
    </div>
  );
}

export default ContactPage;
