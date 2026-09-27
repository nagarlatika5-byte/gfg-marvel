from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)


# =========================
# DATABASE SETUP
# =========================

def init_db():
    conn = sqlite3.connect("registrations.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            branch TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# MAIN WEBSITE
# =========================

@app.route("/")
def home():

    return """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>GFG × MARVEL | The Assembly</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            background: #050505;
            color: white;
            font-family: "Space Grotesk", sans-serif;
            overflow-x: hidden;
        }

        ::selection {
            background: #e50914;
            color: white;
        }

        /* =========================
           CURSOR GLOW
        ========================= */

        .cursor-glow {
            position: fixed;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            pointer-events: none;
            background: radial-gradient(
                circle,
                rgba(229, 9, 20, 0.13),
                transparent 65%
            );
            transform: translate(-50%, -50%);
            z-index: 9999;
            mix-blend-mode: screen;
        }


        /* =========================
           INTRO
        ========================= */

        .intro {
            position: fixed;
            inset: 0;
            background: #050505;
            z-index: 10000;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            animation: introOut 1.2s ease forwards;
            animation-delay: 2.5s;
        }

        .intro img {
            width: 150px;
            margin-bottom: 25px;
            animation: logoPulse 1.5s ease infinite;
        }

        .intro h1 {
            font-family: "Bebas Neue", sans-serif;
            font-size: clamp(50px, 9vw, 120px);
            letter-spacing: 8px;
        }

        .intro p {
            color: #aaa;
            letter-spacing: 5px;
            margin-top: 5px;
            font-size: 12px;
        }

        @keyframes logoPulse {

            0%, 100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.08);
            }
        }

        @keyframes introOut {

            to {
                opacity: 0;
                visibility: hidden;
                pointer-events: none;
            }
        }


        /* =========================
           NAVBAR
        ========================= */

        nav {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 80px;

            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: 0 6%;

            z-index: 1000;

            background: linear-gradient(
                to bottom,
                rgba(0,0,0,0.85),
                transparent
            );

            backdrop-filter: blur(5px);
        }

        .nav-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .nav-logo img {
            width: 48px;
        }

        .nav-logo span {
            font-weight: 700;
            letter-spacing: 2px;
            font-size: 13px;
        }

        .nav-links {
            display: flex;
            gap: 35px;
            list-style: none;
        }

        .nav-links a {
            color: white;
            text-decoration: none;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 1.5px;
            position: relative;
        }

        .nav-links a::after {
            content: "";
            position: absolute;
            bottom: -7px;
            left: 0;
            width: 0;
            height: 2px;
            background: #e50914;
            transition: 0.3s;
        }

        .nav-links a:hover::after {
            width: 100%;
        }


        /* =========================
           HERO
        ========================= */

        .hero {
            height: 100vh;
            min-height: 650px;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
        }

        .hero-video {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: 0;
            transform: scale(1.05);
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: 0;

            background:
                linear-gradient(
                    90deg,
                    rgba(0,0,0,0.92) 0%,
                    rgba(0,0,0,0.62) 45%,
                    rgba(0,0,0,0.25) 100%
                ),
                linear-gradient(
                    0deg,
                    #050505 0%,
                    transparent 35%
                );

            z-index: 1;
        }

        .hero-content {
            position: relative;
            z-index: 2;
            padding: 0 8%;
            max-width: 900px;
        }

        .eyebrow {
            color: #e50914;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 5px;
            margin-bottom: 20px;
        }

        .hero h1 {
            font-family: "Bebas Neue", sans-serif;
            font-size: clamp(80px, 14vw, 190px);
            line-height: 0.82;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .hero h1 span {
            color: #e50914;
        }

        .hero-subtitle {
            margin-top: 30px;
            max-width: 580px;
            color: #d0d0d0;
            line-height: 1.7;
            font-size: 15px;
        }

        .hero-buttons {
            display: flex;
            gap: 15px;
            margin-top: 35px;
            flex-wrap: wrap;
        }

        .btn {
            padding: 15px 25px;
            text-decoration: none;
            font-weight: 700;
            font-size: 12px;
            letter-spacing: 1.5px;
            transition: 0.3s;
            display: inline-block;
        }

        .btn-red {
            background: #e50914;
            color: white;
        }

        .btn-red:hover {
            background: white;
            color: black;
            transform: translateY(-3px);
        }

        .btn-outline {
            border: 1px solid rgba(255,255,255,0.5);
            color: white;
        }

        .btn-outline:hover {
            background: white;
            color: black;
            transform: translateY(-3px);
        }

        .scroll-text {
            position: absolute;
            bottom: 35px;
            left: 8%;
            z-index: 3;
            font-size: 10px;
            letter-spacing: 4px;
            color: #aaa;
        }


        /* =========================
           MARQUEE
        ========================= */

        .marquee {
            background: #e50914;
            color: white;
            overflow: hidden;
            padding: 14px 0;
            white-space: nowrap;
        }

        .marquee-track {
            display: inline-block;
            animation: marquee 20s linear infinite;
            font-family: "Bebas Neue", sans-serif;
            font-size: 28px;
            letter-spacing: 3px;
        }

        @keyframes marquee {

            from {
                transform: translateX(0);
            }

            to {
                transform: translateX(-50%);
            }
        }


        /* =========================
           COMMON SECTION
        ========================= */

        section {
            padding: 120px 8%;
            position: relative;
        }

        .section-label {
            color: #e50914;
            font-size: 11px;
            letter-spacing: 4px;
            font-weight: 700;
            margin-bottom: 20px;
        }

        .section-title {
            font-family: "Bebas Neue", sans-serif;
            font-size: clamp(55px, 8vw, 110px);
            line-height: 0.9;
            letter-spacing: 2px;
        }

        .section-title span {
            color: #e50914;
        }


        /* =========================
           ABOUT
        ========================= */

        .about {
            background:
                radial-gradient(
                    circle at 80% 20%,
                    rgba(229,9,20,0.12),
                    transparent 30%
                ),
                #050505;
        }

        .about-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 70px;
            align-items: center;
        }

        .about-text p {
            color: #aaa;
            line-height: 1.8;
            margin-top: 30px;
            max-width: 600px;
        }

        .about-image {
            position: relative;
            min-height: 500px;
            overflow: hidden;
            border: 1px solid #222;
        }

        .about-image img {
            width: 100%;
            height: 100%;
            min-height: 500px;
            object-fit: cover;
            filter: grayscale(20%) contrast(1.1);
            transition: 0.7s;
        }

        .about-image:hover img {
            transform: scale(1.05);
        }

        .about-image::after {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(
                    to top,
                    rgba(0,0,0,0.9),
                    transparent 55%
                );
        }

        .about-overlay {
            position: absolute;
            bottom: 35px;
            left: 35px;
            z-index: 2;
        }

        .about-overlay h3 {
            font-family: "Bebas Neue", sans-serif;
            font-size: 50px;
            line-height: 0.9;
        }

        .about-overlay h3 span {
            color: #e50914;
        }


        /* =========================
           CHARACTERS
        ========================= */

        .characters {
            background: #080808;
        }

        .character-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 70px;
        }

        .character-card {
            height: 560px;
            position: relative;
            overflow: hidden;
            border: 1px solid #222;
            transform-style: preserve-3d;
            transition: transform 0.2s ease;
        }

        .character-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: 0.7s;
        }

        .character-card::after {
            content: "";
            position: absolute;
            inset: 0;

            background:
                linear-gradient(
                    to top,
                    rgba(0,0,0,0.95),
                    transparent 55%
                );
        }

        .character-card:hover img {
            transform: scale(1.08);
        }

        .character-info {
            position: absolute;
            z-index: 2;
            bottom: 30px;
            left: 30px;
            right: 20px;
        }

        .character-number {
            color: #e50914;
            font-size: 11px;
            letter-spacing: 3px;
        }

        .character-info h3 {
            font-family: "Bebas Neue", sans-serif;
            font-size: 48px;
            margin: 5px 0;
        }

        .character-info p {
            color: #bbb;
            font-size: 12px;
        }


        /* =========================
           HIGHLIGHTS
        ========================= */

        .highlights {
            background: #050505;
        }

        .highlight-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 70px;
        }

        .highlight {
            min-height: 250px;
            padding: 40px;
            border: 1px solid #222;
            background: linear-gradient(
                135deg,
                #101010,
                #070707
            );
            transition: 0.4s;
        }

        .highlight:hover {
            border-color: #e50914;
            transform: translateY(-8px);
        }

        .highlight span {
            color: #e50914;
            font-family: "Bebas Neue", sans-serif;
            font-size: 50px;
        }

        .highlight h3 {
            margin: 20px 0 10px;
            font-size: 24px;
        }

        .highlight p {
            color: #888;
            line-height: 1.6;
        }


        /* =========================
           SCHEDULE
        ========================= */

        .schedule {
            background: #090909;
        }

        .timeline {
            margin-top: 70px;
            border-left: 1px solid #333;
        }

        .timeline-item {
            padding: 0 0 50px 40px;
            position: relative;
        }

        .timeline-item::before {
            content: "";
            position: absolute;
            width: 10px;
            height: 10px;
            background: #e50914;
            border-radius: 50%;
            left: -5px;
            top: 5px;
            box-shadow: 0 0 20px rgba(229,9,20,0.7);
        }

        .timeline-time {
            color: #e50914;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
        }

        .timeline-item h3 {
            font-size: 25px;
            margin: 10px 0;
        }

        .timeline-item p {
            color: #888;
        }


        /* =========================
           REGISTER
        ========================= */

        .register {
            background:
                radial-gradient(
                    circle at 50% 0%,
                    rgba(229,9,20,0.2),
                    transparent 45%
                ),
                #050505;
            text-align: center;
        }

        .register p {
            color: #999;
            max-width: 600px;
            margin: 25px auto 50px;
            line-height: 1.7;
        }

        .register-form {
            max-width: 600px;
            margin: auto;
            display: grid;
            gap: 15px;
        }

        .register-form input,
        .register-form select {
            width: 100%;
            padding: 17px;
            background: #101010;
            border: 1px solid #292929;
            color: white;
            font-family: inherit;
            outline: none;
        }

        .register-form input:focus,
        .register-form select:focus {
            border-color: #e50914;
        }

        .register-form button {
            border: none;
            cursor: pointer;
            padding: 18px;
            background: #e50914;
            color: white;
            font-weight: 700;
            letter-spacing: 2px;
            transition: 0.3s;
        }

        .register-form button:hover {
            background: white;
            color: black;
        }


        /* =========================
           FOOTER
        ========================= */

        footer {
            border-top: 1px solid #1d1d1d;
            padding: 40px 8%;
            display: flex;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
            color: #666;
            font-size: 12px;
        }

        footer strong {
            color: white;
        }


        /* =========================
           REVEAL ANIMATION
        ========================= */

        .reveal {
            opacity: 0;
            transform: translateY(40px);
            transition: 1s ease;
        }

        .reveal.active {
            opacity: 1;
            transform: translateY(0);
        }


        /* =========================
           MOBILE
        ========================= */

        @media (max-width: 900px) {

            .nav-links {
                gap: 15px;
            }

            .nav-links a {
                font-size: 10px;
            }

            .about-grid {
                grid-template-columns: 1fr;
            }

            .character-grid {
                grid-template-columns: 1fr;
            }

            .highlight-grid {
                grid-template-columns: 1fr;
            }

            .character-card {
                height: 500px;
            }
        }


        @media (max-width: 600px) {

            nav {
                height: 70px;
                padding: 0 5%;
            }

            .nav-logo span {
                display: none;
            }

            .nav-links {
                gap: 12px;
            }

            .nav-links a {
                font-size: 8px;
                letter-spacing: 1px;
            }

            section {
                padding: 90px 6%;
            }

            .hero-content {
                padding: 0 6%;
            }

            .hero h1 {
                font-size: 80px;
            }

            .hero-subtitle {
                font-size: 13px;
            }

            .about-image {
                min-height: 400px;
            }

            .about-image img {
                min-height: 400px;
            }

            .about-overlay h3 {
                font-size: 40px;
            }

            .character-card {
                height: 450px;
            }

            .character-info h3 {
                font-size: 40px;
            }

            footer {
                flex-direction: column;
            }

        }

    </style>

</head>


<body>


<!-- =========================
     INTRO
========================= -->

<div class="intro">

    <img src="/static/image/gfg.png">

    <h1>THE ASSEMBLY</h1>

    <p>GFG × MARVEL</p>

</div>


<!-- CURSOR -->

<div class="cursor-glow"></div>


<!-- =========================
     NAVBAR
========================= -->

<nav>

    <div class="nav-logo">

        <img src="/static/image/gfg.png">

        <span>GFG × MARVEL</span>

    </div>


    <ul class="nav-links">

        <li>
            <a href="#about">ABOUT</a>
        </li>

        <li>
            <a href="#heroes">HEROES</a>
        </li>

        <li>
            <a href="#highlights">HIGHLIGHTS</a>
        </li>

        <li>
            <a href="#register">REGISTER</a>
        </li>

    </ul>

</nav>


<!-- =========================
     HERO
========================= -->

<section class="hero">

    <video
        class="hero-video"
        autoplay
        muted
        loop
        playsinline
    >

        <source
            src="/static/videos/hero.mp4"
            type="video/mp4"
        >

    </video>


    <div class="hero-content reveal">

        <div class="eyebrow">
            BENNETT UNIVERSITY • GFG STUDENT CHAPTER
        </div>

        <h1>
            THE<br>
            <span>ASSEMBLY</span>
        </h1>

        <p class="hero-subtitle">

            Where technology meets imagination.
            Assemble your skills, challenge your limits
            and step into a world inspired by the greatest
            heroes of the Marvel universe.

        </p>


        <div class="hero-buttons">

            <a
                href="#register"
                class="btn btn-red"
            >
                JOIN THE ASSEMBLY
            </a>

            <a
                href="#about"
                class="btn btn-outline"
            >
                EXPLORE
            </a>

        </div>

    </div>


    <div class="scroll-text">
        SCROLL TO EXPLORE ↓
    </div>

</section>


<!-- =========================
     MARQUEE
========================= -->

<div class="marquee">

    <div class="marquee-track">

        CODE • CREATE • COMPETE • INNOVATE • ASSEMBLE •
        CODE • CREATE • COMPETE • INNOVATE • ASSEMBLE •

    </div>

</div>


<!-- =========================
     ABOUT
========================= -->

<section
    class="about"
    id="about"
>

    <div class="about-grid">


        <div class="about-text reveal">

            <div class="section-label">
                01 — THE MISSION
            </div>

            <h2 class="section-title">

                WHERE<br>
                <span>HEROES</span><br>
                MEET CODE.

            </h2>


            <p>

                The Assembly is a Marvel-inspired
                technology experience created for
                curious minds, builders and future
                innovators.

                <br><br>

                Bring your ideas. Bring your skills.
                Bring your team.

                <br><br>

                It's time to assemble.

            </p>

        </div>


        <div class="about-image reveal">

            <img
                src="/static/image/hero.jpg"
                alt="Marvel inspired event"
            >

            <div class="about-overlay">

                <h3>
                    WHERE<br>
                    <span>HEROES</span><br>
                    MEET CODE.
                </h3>

            </div>

        </div>

    </div>

</section>


<!-- =========================
     HEROES
========================= -->

<section
    class="characters"
    id="heroes"
>

    <div class="section-label reveal">
        02 — THE HEROES
    </div>

    <h2 class="section-title reveal">

        CHOOSE<br>
        YOUR <span>HERO.</span>

    </h2>


    <div class="character-grid">


        <!-- BLACK PANTHER -->

        <div class="character-card reveal">

            <img
                src="/static/image/blackpanther.jpg"
                alt="Black Panther"
            >

            <div class="character-info">

                <div class="character-number">
                    01 / WAKANDA
                </div>

                <h3>
                    BLACK PANTHER
                </h3>

                <p>
                    Strategy • Leadership • Innovation
                </p>

            </div>

        </div>


        <!-- DOCTOR STRANGE -->

        <div class="character-card reveal">

            <img
                src="/static/image/dr.jpg"
                alt="Doctor Strange"
            >

            <div class="character-info">

                <div class="character-number">
                    02 / MYSTIC ARTS
                </div>

                <h3>
                    DOCTOR STRANGE
                </h3>

                <p>
                    Intelligence • Logic • Vision
                </p>

            </div>

        </div>


        <!-- CAPTAIN AMERICA -->

        <div class="character-card reveal">

            <img
                src="/static/image/captain.jpg"
                alt="Captain America"
            >

            <div class="character-info">

                <div class="character-number">
                    03 / AVENGERS
                </div>

                <h3>
                    CAPTAIN AMERICA
                </h3>

                <p>
                    IRON MAN • SPIDER-MAN
                </p>

            </div>

        </div>

    </div>

</section>


<!-- =========================
     HIGHLIGHTS
========================= -->

<section
    class="highlights"
    id="highlights"
>

    <div class="section-label reveal">
        03 — EXPERIENCE
    </div>

    <h2 class="section-title reveal">

        WHAT'S<br>
        <span>WAITING</span>

    </h2>


    <div class="highlight-grid">


        <div class="highlight reveal">

            <span>01</span>

            <h3>
                TECH CHALLENGES
            </h3>

            <p>
                Test your problem-solving skills
                through exciting technology-driven
                challenges.
            </p>

        </div>


        <div class="highlight reveal">

            <span>02</span>

            <h3>
                TEAM ASSEMBLY
            </h3>

            <p>
                Find your squad and build something
                powerful together.
            </p>

        </div>


        <div class="highlight reveal">

            <span>03</span>

            <h3>
                CREATIVE ARENA
            </h3>

            <p>
                Turn your imagination into something
                real through design and technology.
            </p>

        </div>


        <div class="highlight reveal">

            <span>04</span>

            <h3>
                HERO MOMENTS
            </h3>

            <p>
                Experience a cinematic environment
                designed to make the event memorable.
            </p>

        </div>

    </div>

</section>


<!-- =========================
     SCHEDULE
========================= -->

<section class="schedule">

    <div class="section-label reveal">
        04 — TIMELINE
    </div>

    <h2 class="section-title reveal">

        THE<br>
        <span>MISSION.</span>

    </h2>


    <div class="timeline">


        <div class="timeline-item reveal">

            <div class="timeline-time">
                PHASE 01
            </div>

            <h3>
                ASSEMBLE
            </h3>

            <p>
                Meet the team and prepare for the mission.
            </p>

        </div>


        <div class="timeline-item reveal">

            <div class="timeline-time">
                PHASE 02
            </div>

            <h3>
                DISCOVER
            </h3>

            <p>
                Explore challenges, ideas and opportunities.
            </p>

        </div>


        <div class="timeline-item reveal">

            <div class="timeline-time">
                PHASE 03
            </div>

            <h3>
                BUILD
            </h3>

            <p>
                Work together and turn ideas into reality.
            </p>

        </div>


        <div class="timeline-item reveal">

            <div class="timeline-time">
                PHASE 04
            </div>

            <h3>
                UNLEASH
            </h3>

            <p>
                Showcase what your team created.
            </p>

        </div>

    </div>

</section>


<!-- =========================
     REGISTER
========================= -->

<section
    class="register"
    id="register"
>

    <div class="section-label reveal">
        05 — JOIN THE ASSEMBLY
    </div>


    <h2 class="section-title reveal">

        READY<br>
        TO <span>ASSEMBLE?</span>

    </h2>


    <p class="reveal">

        Enter your details below and become
        part of the experience.

    </p>


    <form
        class="register-form reveal"
        action="/register"
        method="POST"
    >

        <input
            type="text"
            name="name"
            placeholder="FULL NAME"
            required
        >


        <input
            type="email"
            name="email"
            placeholder="EMAIL ADDRESS"
            required
        >


        <select
            name="branch"
            required
        >

            <option value="">
                SELECT BRANCH
            </option>

            <option value="CSE">
                CSE
            </option>

            <option value="AI">
                AI / ML
            </option>

            <option value="ECE">
                ECE
            </option>

            <option value="IT">
                IT
            </option>

            <option value="BBA">
                BBA
            </option>

            <option value="OTHER">
                OTHER
            </option>

        </select>


        <button type="submit">
            REGISTER NOW →
        </button>

    </form>

</section>


<!-- =========================
     FOOTER
========================= -->

<footer>

    <div>
        <strong>GFG × MARVEL</strong>
        <br>
        The Assembly
    </div>

    <div>
        BENNETT UNIVERSITY
    </div>

    <div>
        © 2026 GFG STUDENT CHAPTER
    </div>

</footer>


<!-- =========================
     JAVASCRIPT
========================= -->

<script>


/* =========================
   CURSOR
========================= */

const cursor = document.querySelector(".cursor-glow");

document.addEventListener("mousemove", function(e) {

    cursor.style.left = e.clientX + "px";
    cursor.style.top = e.clientY + "px";

});


/* =========================
   SCROLL REVEAL
========================= */

const reveals = document.querySelectorAll(".reveal");


function revealOnScroll() {

    const windowHeight = window.innerHeight;

    reveals.forEach(function(element) {

        const elementTop =
            element.getBoundingClientRect().top;

        if (elementTop < windowHeight - 80) {

            element.classList.add("active");

        }

    });

}


window.addEventListener(
    "scroll",
    revealOnScroll
);

revealOnScroll();


/* =========================
   HERO PARALLAX
========================= */

const heroVideo =
    document.querySelector(".hero-video");


window.addEventListener("scroll", function() {

    const scroll =
        window.scrollY;

    if (heroVideo) {

        heroVideo.style.transform =
            "scale(1.05) translateY(" +
            scroll * 0.08 +
            "px)";

    }

});


/* =========================
   3D CHARACTER CARDS
========================= */

const cards =
    document.querySelectorAll(".character-card");


cards.forEach(function(card) {

    card.addEventListener(
        "mousemove",
        function(e) {

            const rect =
                card.getBoundingClientRect();

            const x =
                e.clientX - rect.left;

            const y =
                e.clientY - rect.top;

            const centerX =
                rect.width / 2;

            const centerY =
                rect.height / 2;

            const rotateX =
                ((y - centerY) / centerY) * -5;

            const rotateY =
                ((x - centerX) / centerX) * 5;


            card.style.transform =
                "perspective(900px) rotateX(" +
                rotateX +
                "deg) rotateY(" +
                rotateY +
                "deg) scale(1.02)";

        }
    );


    card.addEventListener(
        "mouseleave",
        function() {

            card.style.transform =
                "perspective(900px) rotateX(0) rotateY(0) scale(1)";

        }
    );

});


</script>


</body>

</html>
"""


# =========================
# REGISTRATION
# =========================

@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    email = request.form.get("email")
    branch = request.form.get("branch")

    if name and email and branch:

        conn = sqlite3.connect("registrations.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO registrations
            (name, email, branch)
            VALUES (?, ?, ?)
            """,
            (name, email, branch)
        )

        conn.commit()
        conn.close()

    return redirect("/#register")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )