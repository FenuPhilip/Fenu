#!/usr/bin/env python3
"""Script to write the redesigned home.html for the Fenu portfolio."""

import pathlib

TARGET = pathlib.Path(r"c:\Users\Fenu Philip\Desktop\fenu\templates\home.html")

HTML = """\
<!DOCTYPE html>
{% load video_filters %}
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ profile.name }} \u2014 Portfolio</title>
    <meta name="description" content="{{ profile.role }} \u2014 {{ profile.bio|truncatewords:30 }}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400;1,9..144,500;1,9..144,700&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">

    <style>
    /* ============================================================
       DESIGN SYSTEM \u2014 Deep Obsidian + Electric Violet
    ============================================================ */
    :root {
        --bg:              #0d0d12;
        --bg-2:            #111118;
        --bg-3:            #16161f;
        --bg-4:            #1c1c28;
        --bg-5:            #222232;
        --glass:           rgba(255,255,255,0.035);
        --glass-hover:     rgba(255,255,255,0.06);
        --glass-border:    rgba(255,255,255,0.07);
        --glass-border-h:  rgba(255,255,255,0.14);
        --accent:          #7c3aed;
        --accent-2:        #9d61f7;
        --accent-3:        #c084fc;
        --accent-glow:     rgba(124,58,237,0.35);
        --accent-dim:      rgba(124,58,237,0.12);
        --accent-subtle:   rgba(124,58,237,0.06);
        --lime:            #a3e635;
        --lime-dim:        rgba(163,230,53,0.12);
        --text:            #f0eeff;
        --text-2:          #b8b4d4;
        --text-3:          #7a7697;
        --text-4:          #4a4762;
        --border:          rgba(255,255,255,0.06);
        --border-2:        rgba(255,255,255,0.10);
        --border-3:        rgba(255,255,255,0.16);
        --font-display:    'Fraunces', Georgia, serif;
        --font-body:       'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono:       'JetBrains Mono', 'Courier New', monospace;
        --sidebar-w:       268px;
        --radius:          14px;
        --radius-sm:       9px;
        --radius-pill:     100px;
        --transition:      .22s cubic-bezier(.4,0,.2,1);
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }

    body {
        font-family: var(--font-body);
        background: var(--bg);
        color: var(--text);
        min-height: 100vh;
        overflow-x: hidden;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--bg-5); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    a { text-decoration: none; color: inherit; }
    img { display: block; max-width: 100%; }
    button { cursor: pointer; border: none; background: none; font-family: inherit; }

    /* ---- PAGE LAYOUT ---- */
    .page-wrap { display: flex; min-height: 100vh; }

    /* ---- SIDEBAR ---- */
    .sidebar {
        width: var(--sidebar-w);
        min-width: var(--sidebar-w);
        position: fixed;
        top: 0; left: 0; bottom: 0;
        z-index: 100;
        padding: 20px 16px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        overflow-y: auto;
        overflow-x: hidden;
        scrollbar-width: none;
        border-right: 1px solid var(--border);
        background: linear-gradient(180deg, rgba(13,13,18,0.98) 0%, rgba(17,17,24,0.96) 100%);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
    }
    .sidebar::-webkit-scrollbar { display: none; }

    .sb-card {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius);
        padding: 16px;
        transition: border-color var(--transition);
    }
    .sb-card:hover { border-color: var(--glass-border-h); }

    .sb-identity { display: flex; flex-direction: column; gap: 14px; padding: 18px; }
    .sb-top-row { display: flex; align-items: center; justify-content: space-between; }

    .sb-name-badge {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
        color: #fff;
        font-family: var(--font-body);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.06em;
        padding: 5px 12px;
        border-radius: var(--radius-sm);
        display: inline-flex;
        align-items: center;
        gap: 2px;
        text-transform: uppercase;
        box-shadow: 0 4px 16px var(--accent-glow);
    }
    .sb-name-badge sup { font-size: 7px; vertical-align: super; margin-left: 1px; opacity: 0.75; }

    .sb-social-row { display: flex; gap: 6px; }

    .sb-social-icon {
        width: 30px; height: 30px;
        border-radius: var(--radius-sm);
        background: var(--glass);
        border: 1px solid var(--border);
        display: flex; align-items: center; justify-content: center;
        transition: var(--transition);
        color: var(--text-3);
    }
    .sb-social-icon:hover {
        background: var(--accent-dim);
        border-color: var(--accent);
        color: var(--accent-3);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px var(--accent-glow);
    }
    .sb-social-icon svg { width: 13px; height: 13px; fill: currentColor; }

    .sb-avatar {
        width: 40px; height: 40px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid var(--accent);
        box-shadow: 0 0 0 4px var(--accent-dim);
    }

    .sb-desc { font-size: 12px; line-height: 1.65; color: var(--text-3); font-weight: 400; }

    .sb-stats { display: flex; align-items: center; padding: 14px 18px; }
    .sb-stat { flex: 1; text-align: center; }

    .sb-stat-number {
        font-family: var(--font-display);
        font-size: 26px;
        font-weight: 700;
        font-style: italic;
        background: linear-gradient(135deg, var(--accent-3) 0%, var(--lime) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        margin-bottom: 4px;
    }

    .sb-stat-label { font-size: 10px; font-weight: 600; color: var(--text-4); letter-spacing: 0.1em; text-transform: uppercase; }
    .sb-stats-sep { width: 1px; height: 36px; background: var(--border-2); margin: 0 6px; }

    .sb-nav { display: flex; flex-direction: column; gap: 3px; padding: 10px 8px; }

    .sb-nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 9px 14px;
        border-radius: var(--radius-sm);
        font-size: 11.5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: var(--text-3);
        transition: var(--transition);
        position: relative;
    }
    .sb-nav-item:hover { background: var(--glass-hover); color: var(--text); }
    .sb-nav-item.active {
        background: var(--accent-dim);
        color: var(--accent-3);
        border: 1px solid rgba(124,58,237,0.25);
    }
    .sb-nav-item.active::before {
        content: '';
        position: absolute;
        left: 0; top: 50%;
        transform: translateY(-50%);
        width: 3px; height: 18px;
        background: linear-gradient(180deg, var(--accent) 0%, var(--accent-3) 100%);
        border-radius: 0 3px 3px 0;
    }
    .sb-nav-item svg { width: 13px; height: 13px; flex-shrink: 0; fill: currentColor; }

    .sb-email {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 11px 14px;
        font-family: var(--font-mono);
        font-size: 10.5px;
        color: var(--text-3);
        letter-spacing: 0.02em;
        cursor: pointer;
        transition: var(--transition);
        border-radius: var(--radius);
    }
    .sb-email:hover { background: var(--glass-hover); color: var(--accent-3); }

    .sb-email-icon {
        width: 15px; height: 15px;
        fill: none;
        stroke: currentColor;
        stroke-width: 1.5;
        transition: var(--transition);
        flex-shrink: 0;
    }

    .sb-email-toast {
        position: fixed;
        bottom: 28px; left: 50%;
        transform: translateX(-50%) translateY(20px);
        background: var(--bg-5);
        border: 1px solid var(--accent);
        color: var(--accent-3);
        font-family: var(--font-mono);
        font-size: 11px;
        padding: 10px 22px;
        border-radius: var(--radius-pill);
        opacity: 0;
        pointer-events: none;
        transition: opacity .3s, transform .3s;
        z-index: 9999;
        box-shadow: 0 8px 32px var(--accent-glow);
    }
    .sb-email-toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }

    .sb-cta {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        width: 100%;
        padding: 13px 20px;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
        color: #fff;
        font-family: var(--font-body);
        font-size: 13px;
        font-weight: 700;
        border-radius: var(--radius);
        border: none;
        cursor: pointer;
        transition: var(--transition);
        letter-spacing: 0.04em;
        box-shadow: 0 4px 20px var(--accent-glow);
        position: relative;
        overflow: hidden;
    }
    .sb-cta::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, transparent 60%);
        opacity: 0;
        transition: opacity var(--transition);
    }
    .sb-cta:hover::before { opacity: 1; }
    .sb-cta:hover { transform: translateY(-2px); box-shadow: 0 8px 32px var(--accent-glow); }
    .sb-cta:active { transform: scale(0.98); }

    .sb-visits {
        font-family: var(--font-mono);
        font-size: 9.5px;
        color: var(--text-4);
        text-align: center;
        padding: 4px 0 2px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* ---- MAIN CONTENT ---- */
    .main-content { flex: 1; margin-left: var(--sidebar-w); min-width: 0; }

    /* ---- HERO ---- */
    .hero {
        padding: 90px 64px 72px;
        min-height: 65vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
        background: var(--bg);
    }
    .hero::before {
        content: '';
        position: absolute;
        width: 600px; height: 600px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(124,58,237,0.18) 0%, transparent 70%);
        top: -100px; right: -100px;
        pointer-events: none;
    }
    .hero::after {
        content: '';
        position: absolute;
        width: 400px; height: 400px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(163,230,53,0.08) 0%, transparent 70%);
        bottom: -80px; left: 30%;
        pointer-events: none;
    }

    .hero-label {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--accent-3);
        border: 1px solid rgba(124,58,237,0.3);
        background: var(--accent-subtle);
        padding: 6px 16px;
        border-radius: var(--radius-pill);
        margin-bottom: 32px;
        width: fit-content;
    }
    .hero-label::before {
        content: '';
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--accent-3);
        box-shadow: 0 0 8px var(--accent-3);
        animation: pulse-dot 2s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.8); }
    }

    .hero h1 {
        font-family: var(--font-display);
        font-size: clamp(44px, 5.5vw, 82px);
        font-weight: 400;
        font-style: italic;
        line-height: 1.06;
        letter-spacing: -0.02em;
        color: var(--text);
        max-width: 780px;
        margin-bottom: 28px;
    }

    .hero-sub { font-size: 16px; line-height: 1.7; color: var(--text-2); max-width: 500px; font-weight: 400; }

    .hero-bg-img {
        position: absolute;
        top: 50%; right: 6%;
        transform: translateY(-50%);
        width: 420px; height: 420px;
        object-fit: cover;
        border-radius: 50%;
        filter: blur(64px) saturate(0.5);
        opacity: 0.15;
        pointer-events: none;
        z-index: 0;
    }

    /* ---- SECTION HEADERS ---- */
    .section-header { padding: 0 64px; margin-bottom: 44px; }

    .section-label {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: var(--font-mono);
        font-size: 10.5px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        padding: 5px 14px;
        border-radius: var(--radius-pill);
        margin-bottom: 22px;
        width: fit-content;
    }
    .section-label::before { content: '//'; font-size: 9px; opacity: 0.5; }
    .section-label.light,
    .section-label.dark {
        color: var(--accent-3);
        background: var(--accent-subtle);
        border: 1px solid rgba(124,58,237,0.2);
    }

    .section-heading {
        font-family: var(--font-display);
        font-size: clamp(34px, 4vw, 62px);
        font-weight: 400;
        font-style: italic;
        line-height: 1.08;
        letter-spacing: -0.015em;
        color: var(--text);
        margin-bottom: 16px;
    }

    .section-desc { font-size: 15px; line-height: 1.7; max-width: 480px; font-weight: 400; color: var(--text-2); }

    /* ---- PROJECTS SECTION ---- */
    .projects-section {
        background: var(--bg-2);
        padding: 80px 0 90px;
        position: relative;
        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
    }
    .projects-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--accent) 30%, var(--accent-3) 70%, transparent 100%);
        opacity: 0.4;
    }

    .filters { display: flex; gap: 6px; padding: 0 64px; margin-bottom: 40px; flex-wrap: wrap; }
    .filters button {
        padding: 7px 20px;
        border-radius: var(--radius-pill);
        font-family: var(--font-mono);
        font-size: 10.5px;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-3);
        border: 1px solid var(--border-2);
        background: transparent;
        transition: var(--transition);
    }
    .filters button:hover { color: var(--text); border-color: var(--border-3); background: var(--glass); }
    .filters button.active { background: var(--accent-dim); border-color: rgba(124,58,237,0.4); color: var(--accent-3); }

    .feed {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
        gap: 16px;
        padding: 0 64px;
    }

    .post {
        background: var(--bg-3);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        transition: border-color var(--transition), transform var(--transition), box-shadow var(--transition);
        animation: fadeUp .55s cubic-bezier(.22,1,.36,1) both;
        position: relative;
    }
    .post:hover {
        border-color: rgba(124,58,237,0.3);
        transform: translateY(-4px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,58,237,0.15);
    }

    .post-inner { padding: 22px; }

    .post-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: var(--radius-pill);
        font-family: var(--font-mono);
        font-size: 9.5px;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    .badge::before { content: ''; width: 5px; height: 5px; border-radius: 50%; }
    .badge.project { background: var(--accent-dim); border: 1px solid rgba(124,58,237,0.3); color: var(--accent-3); }
    .badge.project::before { background: var(--accent-3); box-shadow: 0 0 6px var(--accent-3); }
    .badge.event { background: rgba(163,230,53,0.08); border: 1px solid rgba(163,230,53,0.25); color: var(--lime); }
    .badge.event::before { background: var(--lime); box-shadow: 0 0 6px var(--lime); }

    .post-serial {
        font-family: var(--font-mono);
        font-size: 10px;
        color: var(--text-4);
        letter-spacing: 0.06em;
        background: var(--glass);
        padding: 4px 10px;
        border-radius: var(--radius-pill);
        border: 1px solid var(--border);
    }

    .post-media-wrap { margin: 0 -22px 18px; overflow: hidden; position: relative; }
    .post-media { width: 100%; max-height: 300px; object-fit: cover; display: block; transition: transform .6s cubic-bezier(.4,0,.2,1); }
    .post:hover .post-media { transform: scale(1.04); }
    .post video { width: calc(100% + 44px); margin: 0 -22px 18px; display: block; }
    .post-caption { font-size: 13.5px; line-height: 1.7; color: var(--text-2); font-weight: 400; }

    .social-embed { margin-bottom: 16px; }
    .instagram-media { max-width: 100% !important; }
    .youtube-container { overflow: hidden; aspect-ratio: 16/9; border-radius: var(--radius-sm); margin: 0 -22px 18px; width: calc(100% + 44px); }
    .youtube-container iframe { width: 100%; height: 100%; border: none; display: block; }
    .social-embed iframe, .social-embed blockquote { width: 100%; }

    .linkedin-preview { padding: 14px 18px; background: rgba(10,102,194,0.08); border: 1px solid rgba(10,102,194,0.25); border-left: 3px solid #0A66C2; border-radius: var(--radius-sm); margin-bottom: 16px; }
    .preview-header { font-family: var(--font-mono); font-size: 9.5px; letter-spacing: 0.14em; text-transform: uppercase; color: #4a9eff; margin-bottom: 10px; }
    .linkedin-btn { display: inline-flex; align-items: center; gap: 6px; padding: 7px 16px; background: #0A66C2; color: white; font-family: var(--font-body); font-size: 11px; font-weight: 600; letter-spacing: 0.04em; border-radius: var(--radius-sm); transition: opacity .15s; }
    .linkedin-btn:hover { opacity: 0.85; }

    .ext-link {
        display: inline-flex;
        align-items: center; gap: 8px;
        font-family: var(--font-mono);
        font-size: 10.5px;
        letter-spacing: 0.06em;
        color: var(--text-3);
        padding: 8px 16px;
        background: var(--glass);
        border: 1px solid var(--border-2);
        border-radius: var(--radius-sm);
        transition: var(--transition);
        margin-bottom: 16px;
    }
    .ext-link:hover { border-color: var(--accent); color: var(--accent-3); background: var(--accent-dim); box-shadow: 0 4px 16px var(--accent-glow); }

    /* ---- SKILLS ---- */
    .skills-section { padding: 80px 64px 90px; background: var(--bg); border-top: 1px solid var(--border); }

    .skills-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }

    .skill-card {
        background: var(--glass);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 20px;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    .skill-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        opacity: 0;
        transition: opacity var(--transition);
    }
    .skill-card:hover { background: var(--glass-hover); border-color: rgba(124,58,237,0.25); transform: translateY(-3px); box-shadow: 0 12px 36px rgba(0,0,0,0.3); }
    .skill-card:hover::before { opacity: 1; }

    .skill-name { font-family: var(--font-body); font-size: 13.5px; font-weight: 600; color: var(--text); margin-bottom: 12px; }
    .skill-bar-wrap { height: 2px; background: var(--border-2); border-radius: 2px; overflow: hidden; margin-bottom: 8px; }
    .skill-bar-fill {
        height: 100%;
        border-radius: 2px;
        background: linear-gradient(90deg, var(--accent) 0%, var(--accent-3) 100%);
        transition: width 1s cubic-bezier(.4,0,.2,1);
        box-shadow: 0 0 8px var(--accent-glow);
    }
    .skill-level-text { font-family: var(--font-mono); font-size: 9.5px; color: var(--text-4); letter-spacing: 0.08em; }
    .level-1 { width: 20%; }
    .level-2 { width: 40%; }
    .level-3 { width: 60%; }
    .level-4 { width: 80%; }
    .level-5 { width: 100%; }

    /* ---- CONTACT ---- */
    .contact-section { padding: 80px 64px 90px; background: var(--bg-2); border-top: 1px solid var(--border); }

    .contact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 52px; max-width: 920px; }

    .contact-info h3 { font-family: var(--font-display); font-size: 28px; font-style: italic; font-weight: 400; margin-bottom: 16px; color: var(--text); line-height: 1.25; }
    .contact-info p { font-size: 14px; color: var(--text-3); line-height: 1.7; margin-bottom: 28px; }

    .contact-socials { display: flex; gap: 8px; }
    .contact-socials a { width: 40px; height: 40px; border-radius: var(--radius-sm); background: var(--glass); border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; color: var(--text-3); transition: var(--transition); }
    .contact-socials a:hover { background: var(--accent-dim); border-color: var(--accent); color: var(--accent-3); transform: translateY(-2px); box-shadow: 0 6px 20px var(--accent-glow); }
    .contact-socials a svg { width: 16px; height: 16px; fill: currentColor; }

    .contact-form { display: flex; flex-direction: column; gap: 14px; }
    .field-group { display: flex; flex-direction: column; gap: 6px; }
    .field-label { font-family: var(--font-mono); font-size: 10px; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-4); }

    .contact-form input,
    .contact-form textarea {
        width: 100%;
        padding: 12px 16px;
        background: var(--glass);
        border: 1px solid var(--border-2);
        border-radius: var(--radius-sm);
        color: var(--text);
        font-family: var(--font-body);
        font-size: 14px;
        outline: none;
        transition: border-color .2s, box-shadow .2s, background .2s;
        resize: none;
    }
    .contact-form input::placeholder, .contact-form textarea::placeholder { color: var(--text-4); }
    .contact-form input:focus, .contact-form textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-dim); background: var(--glass-hover); }
    .contact-form textarea { min-height: 100px; resize: vertical; }

    .form-submit {
        width: 100%;
        padding: 14px;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
        color: #fff;
        font-family: var(--font-body);
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.04em;
        border: none;
        border-radius: var(--radius-sm);
        cursor: pointer;
        transition: var(--transition);
        box-shadow: 0 4px 20px var(--accent-glow);
    }
    .form-submit:hover { transform: translateY(-2px); box-shadow: 0 8px 32px var(--accent-glow); }
    .form-submit:active { transform: scale(0.98); }

    /* ---- PANEL ---- */
    .overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(6px); z-index: 998; opacity: 0; pointer-events: none; transition: opacity .3s; }
    .overlay.show { opacity: 1; pointer-events: all; }

    .panel { position: fixed; top: 0; right: -460px; width: 420px; height: 100%; z-index: 999; background: var(--bg-3); border-left: 1px solid var(--border-2); padding: 80px 32px 32px; transition: right .4s cubic-bezier(.4,0,.2,1); overflow-y: auto; display: flex; flex-direction: column; }
    .panel.show { right: 0; }

    .panel-header { margin-bottom: 32px; }
    .panel-label { font-family: var(--font-mono); font-size: 10px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: var(--accent-3); margin-bottom: 10px; }
    .panel h3 { font-family: var(--font-display); font-size: 30px; font-style: italic; font-weight: 400; color: var(--text); line-height: 1.15; }

    .panel .field-group { margin-bottom: 14px; }
    .panel .field-label { font-family: var(--font-mono); font-size: 9.5px; font-weight: 500; letter-spacing: 0.16em; color: var(--text-4); margin-bottom: 6px; display: block; text-transform: uppercase; }
    .panel input, .panel textarea { width: 100%; background: var(--glass); border: 1px solid var(--border-2); border-radius: var(--radius-sm); color: var(--text); padding: 11px 14px; font-family: var(--font-body); font-size: 14px; outline: none; transition: border-color .2s, box-shadow .2s, background .2s; resize: none; }
    .panel input::placeholder, .panel textarea::placeholder { color: var(--text-4); }
    .panel input:focus, .panel textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-dim); background: var(--glass-hover); }
    .panel textarea { min-height: 100px; resize: vertical; }

    .panel-submit { width: 100%; padding: 14px; border: none; cursor: pointer; border-radius: var(--radius-sm); background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%); color: #fff; font-family: var(--font-body); font-size: 14px; font-weight: 700; letter-spacing: 0.04em; transition: var(--transition); margin-top: 8px; box-shadow: 0 4px 20px var(--accent-glow); }
    .panel-submit:hover { transform: translateY(-2px); box-shadow: 0 8px 32px var(--accent-glow); }
    .panel-submit:active { transform: scale(0.98); }

    .panel-close { position: absolute; top: 24px; right: 24px; width: 36px; height: 36px; border-radius: 50%; background: var(--glass); border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; cursor: pointer; transition: var(--transition); color: var(--text-3); font-size: 16px; }
    .panel-close:hover { background: var(--accent-dim); color: var(--accent-3); border-color: var(--accent); }

    /* ---- FOOTER ---- */
    .footer { background: var(--bg); padding: 64px 64px 44px; position: relative; overflow: hidden; border-top: 1px solid var(--border); }

    .footer-watermark {
        font-family: var(--font-display);
        font-size: clamp(60px, 12vw, 180px);
        font-weight: 900;
        font-style: italic;
        background: linear-gradient(135deg, rgba(124,58,237,0.15) 0%, rgba(163,230,53,0.08) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 0.85;
        pointer-events: none;
        user-select: none;
        margin-bottom: 44px;
        letter-spacing: -0.03em;
    }

    .footer-bottom { display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid var(--border); padding-top: 24px; }
    .footer-credit { font-size: 12px; color: var(--text-4); font-weight: 400; }
    .footer-credit strong { color: var(--text-2); font-weight: 600; }
    .footer-visits { font-family: var(--font-mono); font-size: 10.5px; color: var(--text-4); letter-spacing: 0.1em; }

    /* ---- MOBILE ---- */
    .mobile-topbar { display: none; position: fixed; top: 0; left: 0; right: 0; z-index: 200; height: 56px; background: rgba(13,13,18,0.94); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); padding: 0 18px; align-items: center; justify-content: space-between; }
    .mobile-name { font-family: var(--font-body); font-size: 13px; font-weight: 700; color: #fff; background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%); padding: 5px 14px; border-radius: var(--radius-sm); text-transform: uppercase; letter-spacing: 0.06em; }
    .mobile-menu-btn { width: 40px; height: 40px; border-radius: var(--radius-sm); background: var(--glass); border: 1px solid var(--border); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 5px; cursor: pointer; }
    .mobile-menu-btn span { width: 18px; height: 1.5px; background: var(--text-2); border-radius: 1px; transition: var(--transition); }
    .mobile-menu-overlay { display: none; position: fixed; inset: 0; z-index: 199; background: rgba(13,13,18,0.97); backdrop-filter: blur(24px); flex-direction: column; align-items: center; justify-content: center; gap: 20px; opacity: 0; pointer-events: none; transition: opacity .3s; }
    .mobile-menu-overlay.show { opacity: 1; pointer-events: all; }
    .mobile-menu-overlay a { font-family: var(--font-display); font-size: 30px; font-style: italic; color: var(--text-2); transition: var(--transition); }
    .mobile-menu-overlay a:hover { color: var(--accent-3); }

    /* ---- ANIMATIONS ---- */
    @keyframes fadeUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    .anim-fade-up { animation: fadeUp .65s cubic-bezier(.22,1,.36,1) both; }
    .anim-delay-1 { animation-delay: .06s; }
    .anim-delay-2 { animation-delay: .12s; }
    .anim-delay-3 { animation-delay: .18s; }
    .anim-delay-4 { animation-delay: .24s; }
    .anim-delay-5 { animation-delay: .30s; }
    .anim-delay-6 { animation-delay: .36s; }
    .post:nth-child(1) { animation-delay: .04s; }
    .post:nth-child(2) { animation-delay: .09s; }
    .post:nth-child(3) { animation-delay: .14s; }
    .post:nth-child(4) { animation-delay: .19s; }
    .post:nth-child(5) { animation-delay: .24s; }
    .post:nth-child(6) { animation-delay: .29s; }

    /* ---- RESPONSIVE ---- */
    @media (max-width: 900px) {
        .sidebar { display: none; }
        .mobile-topbar { display: flex; }
        .mobile-menu-overlay { display: flex; }
        .main-content { margin-left: 0; }
        .hero { padding: 88px 24px 56px; min-height: 55vh; }
        .hero::before, .hero::after { display: none; }
        .section-header { padding: 0 24px; }
        .filters { padding: 0 24px; }
        .feed { padding: 0 24px; grid-template-columns: 1fr; }
        .skills-section { padding: 56px 24px 64px; }
        .contact-section { padding: 56px 24px 64px; }
        .contact-grid { grid-template-columns: 1fr; gap: 36px; }
        .footer { padding: 44px 24px 36px; }
        .post-media-wrap, .youtube-container { margin-left: 0; margin-right: 0; width: 100%; }
        .post video { margin-left: 0; width: 100%; }
    }

    @media (max-width: 500px) {
        .hero h1 { font-size: 34px; }
        .section-heading { font-size: 30px; }
        .feed { grid-template-columns: 1fr; }
        .skills-grid { grid-template-columns: 1fr 1fr; }
        .footer-watermark { font-size: 46px; }
        .footer-bottom { flex-direction: column; align-items: flex-start; gap: 8px; }
    }
    </style>
</head>
<body>

<div class="mobile-topbar">
    <a href="#hero" class="mobile-name">{{ profile.name }}</a>
    <div class="mobile-menu-btn" onclick="toggleMobileMenu()">
        <span></span><span></span><span></span>
    </div>
</div>

<div class="mobile-menu-overlay" id="mobileMenu">
    <a href="#hero" onclick="toggleMobileMenu()">Home</a>
    <a href="#projects" onclick="toggleMobileMenu()">Projects</a>
    <a href="#skills" onclick="toggleMobileMenu()">Skills</a>
    <a href="#contact" onclick="toggleMobileMenu()">Contact</a>
</div>

<div class="page-wrap">

    <aside class="sidebar">
        <div class="sb-card sb-identity anim-fade-up">
            <div class="sb-top-row">
                <span class="sb-name-badge">{{ profile.name }}<sup>\u00ae</sup></span>
                <div class="sb-social-row">
                    {% if profile.github %}
                    <a href="{{ profile.github }}" target="_blank" class="sb-social-icon" aria-label="GitHub">
                        <svg viewBox="0 0 24 24"><path d="M12 0.297C5.373.297 0 5.67 0 12.297c0 5.302 3.438 9.8 8.205 11.387.6.111.82-.261.82-.579 0-.285-.011-1.04-.017-2.042-3.338.726-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.73.083-.73 1.205.084 1.84 1.237 1.84 1.237 1.07 1.835 2.809 1.305 3.495.998.108-.776.418-1.305.762-1.604-2.665-.304-5.466-1.334-5.466-5.93 0-1.31.47-2.382 1.236-3.222-.124-.303-.536-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.29-1.552 3.297-1.23 3.297-1.23.655 1.653.243 2.874.119 3.176.77.84 1.236 1.912 1.236 3.222 0 4.61-2.804 5.625-5.475 5.921.43.372.815 1.103.815 2.222 0 1.606-.015 2.898-.015 3.293 0 .321.217.694.825.576C20.565 22.092 24 17.598 24 12.297 24 5.67 18.627.297 12 .297z"/></svg>
                    </a>
                    {% endif %}
                    {% if profile.linkedin %}
                    <a href="{{ profile.linkedin }}" target="_blank" class="sb-social-icon" aria-label="LinkedIn">
                        <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.039-1.852-3.039-1.853 0-2.136 1.445-2.136 2.939v5.669H9.351V9h3.413v1.561h.049c.476-.9 1.637-1.852 3.372-1.852 3.604 0 4.268 2.373 4.268 5.459v6.284zM5.337 7.433a2.066 2.066 0 1 1 0-4.132 2.066 2.066 0 0 1 0 4.132zm1.777 13.019H3.559V9h3.555v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.727v20.545C0 23.226.792 24 1.771 24h20.451C23.2 24 24 23.226 24 22.272V1.727C24 .774 23.2 0 22.225 0z"/></svg>
                    </a>
                    {% endif %}
                    {% if profile.instagram %}
                    <a href="{{ profile.instagram }}" target="_blank" class="sb-social-icon" aria-label="Instagram">
                        <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 1.17.054 1.97.24 2.43.403a4.92 4.92 0 0 1 1.72 1.088 4.92 4.92 0 0 1 1.088 1.72c.163.46.35 1.26.403 2.43.058 1.266.07 1.646.07 4.85s-.012 3.584-.07 4.85c-.054 1.17-.24 1.97-.403 2.43a4.92 4.92 0 0 1-1.088 1.72 4.92 4.92 0 0 1-1.72 1.088c-.46.163-1.26.35-2.43.403-1.266.058-1.646.07-4.85.07s-3.584-.012-4.85-.07c-1.17-.054-1.97-.24-2.43-.403a4.92 4.92 0 0 1-1.72-1.088 4.92 4.92 0 0 1-1.088-1.72c-.163-.46-.35-1.26-.403-2.43C2.175 15.747 2.163 15.367 2.163 12s.012-3.584.07-4.85c.054-1.17.24-1.97.403-2.43a4.92 4.92 0 0 1 1.088-1.72 4.92 4.92 0 0 1 1.72-1.088c.46-.163 1.26-.35 2.43-.403C8.416 2.175 8.796 2.163 12 2.163zm0-2.163C8.741 0 8.332.013 7.052.072 5.78.13 4.842.31 4.042.652a6.978 6.978 0 0 0-2.53 1.64A6.978 6.978 0 0 0 .652 4.042C.31 4.842.13 5.78.072 7.052.013 8.332 0 8.741 0 12c0 3.259.013 3.668.072 4.948.058 1.272.238 2.21.58 3.01a6.978 6.978 0 0 0 1.64 2.53 6.978 6.978 0 0 0 2.53 1.64c.8.342 1.738.522 3.01.58C8.332 23.987 8.741 24 12 24s3.668-.013 4.948-.072c1.272-.058 2.21-.238 3.01-.58a6.978 6.978 0 0 0 2.53-1.64 6.978 6.978 0 0 0 1.64-2.53c.342-.8.522-1.738.58-3.01.059-1.28.072-1.689.072-4.948s-.013-3.668-.072-4.948c-.058-1.272-.238-2.21-.58-3.01a6.978 6.978 0 0 0-1.64-2.53A6.978 6.978 0 0 0 19.958.652C19.158.31 18.22.13 16.948.072 15.668.013 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zm0 10.162a3.999 3.999 0 1 1 0-7.998 3.999 3.999 0 0 1 0 7.998zm6.406-11.845a1.44 1.44 0 1 1-2.881 0 1.44 1.44 0 0 1 2.881 0z"/></svg>
                    </a>
                    {% endif %}
                </div>
            </div>
            {% if profile.profile_image %}
            <img class="sb-avatar" src="{{ profile.profile_image|safe_url }}" alt="{{ profile.name }}">
            {% endif %}
            <p class="sb-desc">{{ profile.bio|truncatewords:25 }}</p>
        </div>

        <div class="sb-card sb-stats anim-fade-up anim-delay-1">
            <div class="sb-stat">
                <div class="sb-stat-number">{{ visits }}+</div>
                <div class="sb-stat-label">Visits</div>
            </div>
            <div class="sb-stats-sep"></div>
            <div class="sb-stat">
                <div class="sb-stat-number">{{ skills|length }}+</div>
                <div class="sb-stat-label">Skills</div>
            </div>
        </div>

        <div class="sb-card sb-nav anim-fade-up anim-delay-2">
            <a href="#hero" class="sb-nav-item active" data-nav="hero">
                <svg viewBox="0 0 16 16"><path d="M8 15.998c-1.719 0-3.438.004-5.156-.002C1.391 15.992.265 15.025.029 13.592.003 13.438.002 13.279.002 13.122 0 10.908.002 8.693 0 6.479c-.001-1.05.434-1.863 1.293-2.454C2.97 2.873 4.644 1.718 6.319.563 7.4-.182 8.587-.189 9.662.55c1.687 1.16 3.372 2.32 5.057 3.483.845.583 1.279 1.389 1.279 2.424.001 2.227.004 4.454-.001 6.681-.004 1.46-.957 2.588-2.382 2.83-.171.029-.349.03-.523.03-1.7.002-3.4.001-5.1.001z"/></svg>
                Home
            </a>
            <a href="#projects" class="sb-nav-item" data-nav="projects">
                <svg viewBox="0 0 16 16"><path d="M1.336 8c0-1.105.895-2 2-2h9.333c1.105 0 2 .895 2 2v5.333c0 1.105-.895 2-2 2H3.336c-1.105 0-2-.895-2-2V8z"/><path d="M2.664 4.003c0-.368.298-.667.667-.667h9.333c.368 0 .667.299.667.667 0 .368-.299.666-.667.666H3.33a.667.667 0 0 1-.667-.666z"/><path d="M4 1.331c0-.368.298-.667.667-.667h6.667c.368 0 .666.299.666.667 0 .368-.298.666-.666.666H4.667A.667.667 0 0 1 4 1.33z"/></svg>
                Projects
            </a>
            <a href="#skills" class="sb-nav-item" data-nav="skills">
                <svg viewBox="0 0 16 16"><path d="M3.027 10.505c-.337-.143-.72-.143-1.057 0l-1.078.456c-.304.129-.304.665 0 .793l6.673 2.822a.964.964 0 0 0 .864 0l6.673-2.822c.304-.128.304-.664 0-.793l-1.078-.456a1.447 1.447 0 0 0-1.057 0l-4.38 1.852a1.447 1.447 0 0 1-1.181 0l-4.38-1.852z"/><path d="M3.027 6.802c-.337-.143-.72-.143-1.057 0L.892 7.258c-.304.129-.304.665 0 .793l6.673 2.822a.964.964 0 0 0 .864 0l6.673-2.822c.304-.128.304-.664 0-.793l-1.078-.456a1.447 1.447 0 0 0-1.057 0l-4.38 1.852a1.447 1.447 0 0 1-1.181 0l-4.38-1.852z"/><path d="M7.457.796c.384-.165.8-.165 1.185 0l6.135 2.639c.417.179.417.927 0 1.106L8.642 7.18a.964.964 0 0 1-.864 0L1.32 4.54c-.416-.179-.416-.927 0-1.106L7.457.796z"/></svg>
                Skills
            </a>
            <a href="#contact" class="sb-nav-item" data-nav="contact">
                <svg viewBox="0 0 16 16"><path d="M16 7.499V8.467c-.009.05-.02.1-.027.15-.043.314-.07.632-.131.943C15.221 12.78 12.615 15.327 9.38 15.877c-.291.05-.585.082-.877.123H7.503c-.034-.009-.068-.023-.103-.025-.794-.056-1.558-.24-2.302-.523C1.694 14.154-.441 10.537.077 6.932.352 5.023 1.177 3.389 2.613 2.098 4.519.383 6.765-.278 9.298.106c1.523.23 2.864.887 4.012 1.916 1.38 1.237 2.242 2.773 2.567 4.601.052.291.083.585.123.877zM7.342 9.094c0 .094-.004.188.001.281.018.324.273.589.595.621.325.032.641-.188.71-.51a.98.98 0 0 0-.017-.31c-.023-.38.143-.614.489-.783.881-.428 1.393-1.149 1.496-2.12.207-1.962-1.686-3.437-3.548-2.784-1.055.371-1.787 1.416-1.76 2.517.008.356.279.637.628.65.364.014.663-.243.694-.598.008-.083.012-.166.023-.249.1-.788.888-1.315 1.65-1.108.561.153.941.613.995 1.207.049.535-.265 1.06-.79 1.304-.8.372-1.193 1-.2 1.877zM7.998 11.89a.656.656 0 1 0 0-1.313.656.656 0 0 0 0 1.313z"/></svg>
                FAQ / Contact
            </a>
        </div>

        <div class="sb-card sb-email anim-fade-up anim-delay-3" onclick="copyEmail()" title="Copy email">
            <span id="emailText">{{ profile.name|lower|cut:" " }}@portfolio.io</span>
            <svg class="sb-email-icon" viewBox="0 0 16 16"><path d="M4 4v-1c0-1.1.9-2 2-2h7c1.1 0 2 .9 2 2v7c0 1.1-.9 2-2 2h-1M10 6c0-1.1-.9-2-2-2H3c-1.1 0-2 .9-2 2v7c0 1.1.9 2 2 2h5c1.1 0 2-.9 2-2V6z"/></svg>
        </div>

        <button class="sb-cta anim-fade-up anim-delay-4" onclick="togglePanel()">Contact Me \u2192</button>
        <div class="sb-visits anim-fade-up anim-delay-5">V{{ visits }}.io</div>
    </aside>

    <main class="main-content">

        <section class="hero" id="hero">
            {% if profile.profile_image %}
            <img class="hero-bg-img" src="{{ profile.profile_image|safe_url }}" alt="" aria-hidden="true">
            {% endif %}
            <span class="hero-label anim-fade-up">{{ profile.role }}</span>
            <h1 class="anim-fade-up anim-delay-1">{{ profile.hero_title }}</h1>
            <p class="hero-sub anim-fade-up anim-delay-2">{{ profile.hero_subtitle }}</p>
        </section>

        <section class="projects-section" id="projects">
            <div class="section-header anim-fade-up">
                <span class="section-label dark">Selected Work</span>
                <h2 class="section-heading">Built with Passion,<br>Made to Perform</h2>
                <p class="section-desc">A curated collection of projects, events, and milestones from the journey so far.</p>
            </div>
            <div class="filters anim-fade-up" id="filterBar">
                <button class="active" onclick="filterPosts('all', this)">ALL</button>
                <button onclick="filterPosts('project', this)">PROJECTS</button>
                <button onclick="filterPosts('event', this)">EVENTS</button>
            </div>
            <div class="feed">
            {% for post in posts %}
            <article class="post {{ post.post_type }}" data-type="{{ post.post_type }}">
                <div class="post-inner">
                    <div class="post-header">
                        <div class="badge {{ post.post_type }}">{{ post.post_type|upper }}</div>
                        <span class="post-serial">#{{ forloop.counter|stringformat:"04d" }}</span>
                    </div>
                    {% if post.image %}
                    <div class="post-media-wrap">
                        <img class="post-media" src="{{ post.image|safe_url }}" alt="" loading="lazy">
                    </div>
                    {% endif %}
                    {% if post.video %}
                    <video controls><source src="{{ post.video|safe_url }}"></video>
                    {% endif %}
                    {% if post.external_url %}
                    <div class="social-embed">
                        {% if "instagram.com" in post.external_url %}
                        <blockquote class="instagram-media"><a href="{{ post.external_url }}"></a></blockquote>
                        <script async src="//www.instagram.com/embed.js"></script>
                        {% endif %}
                        {% if "youtube.com" in post.external_url or "youtu.be" in post.external_url %}
                        <div class="youtube-container">
                            <iframe src="https://www.youtube.com/embed/{{ post.external_url|youtube_id }}" allowfullscreen></iframe>
                        </div>
                        {% endif %}
                        {% if "twitter.com" in post.external_url or "x.com" in post.external_url %}
                        <blockquote class="twitter-tweet"><a href="{{ post.external_url }}"></a></blockquote>
                        <script async src="https://platform.twitter.com/widgets.js"></script>
                        {% endif %}
                        {% if "facebook.com" in post.external_url %}
                        <iframe src="https://www.facebook.com/plugins/post.php?href={{ post.external_url }}" width="100%" height="600"></iframe>
                        {% endif %}
                        {% if "linkedin.com" in post.external_url %}
                        <div class="linkedin-preview">
                            <div class="preview-header">LINKEDIN</div>
                            <a href="{{ post.external_url }}" target="_blank" class="linkedin-btn">VIEW POST \u2192</a>
                        </div>
                        {% endif %}
                        {% if "github.com" in post.external_url %}
                        <a href="{{ post.external_url }}" target="_blank" class="ext-link">\u2325 GITHUB REPOSITORY \u2192</a>
                        {% endif %}
                        {% if "medium.com" in post.external_url %}
                        <a href="{{ post.external_url }}" target="_blank" class="ext-link">\u2726 READ ON MEDIUM \u2192</a>
                        {% endif %}
                    </div>
                    {% endif %}
                    <div class="post-caption">{{ post.caption }}</div>
                </div>
            </article>
            {% endfor %}
            </div>
        </section>

        {% if skills %}
        <section class="skills-section" id="skills">
            <div class="section-header" style="padding:0; margin-bottom: 40px;">
                <span class="section-label light">Capabilities</span>
                <h2 class="section-heading">What I Bring<br>to the Table</h2>
            </div>
            <div class="skills-grid">
                {% for skill in skills %}
                <div class="skill-card anim-fade-up">
                    <div class="skill-name">{{ skill.name }}</div>
                    <div class="skill-bar-wrap">
                        <div class="skill-bar-fill level-{{ skill.level }}"></div>
                    </div>
                    <div class="skill-level-text">Level {{ skill.level }}/5{% if skill.category %} \u00b7 {{ skill.category }}{% endif %}</div>
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        <section class="contact-section" id="contact">
            <div class="section-header" style="padding:0; margin-bottom: 40px;">
                <span class="section-label light">Get in Touch</span>
                <h2 class="section-heading">Let's Build<br>Something Together</h2>
            </div>
            <div class="contact-grid">
                <div class="contact-info">
                    <h3>Drop a message and I'll get back to you.</h3>
                    <p>Whether it's a project idea, a collaboration, or just a hello \u2014 I'd love to hear from you.</p>
                    <div class="contact-socials">
                        {% if profile.github %}
                        <a href="{{ profile.github }}" target="_blank" aria-label="GitHub">
                            <svg viewBox="0 0 24 24"><path d="M12 0.297C5.373.297 0 5.67 0 12.297c0 5.302 3.438 9.8 8.205 11.387.6.111.82-.261.82-.579 0-.285-.011-1.04-.017-2.042-3.338.726-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.73.083-.73 1.205.084 1.84 1.237 1.84 1.237 1.07 1.835 2.809 1.305 3.495.998.108-.776.418-1.305.762-1.604-2.665-.304-5.466-1.334-5.466-5.93 0-1.31.47-2.382 1.236-3.222-.124-.303-.536-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.29-1.552 3.297-1.23 3.297-1.23.655 1.653.243 2.874.119 3.176.77.84 1.236 1.912 1.236 3.222 0 4.61-2.804 5.625-5.475 5.921.43.372.815 1.103.815 2.222 0 1.606-.015 2.898-.015 3.293 0 .321.217.694.825.576C20.565 22.092 24 17.598 24 12.297 24 5.67 18.627.297 12 .297z"/></svg>
                        </a>
                        {% endif %}
                        {% if profile.linkedin %}
                        <a href="{{ profile.linkedin }}" target="_blank" aria-label="LinkedIn">
                            <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.039-1.852-3.039-1.853 0-2.136 1.445-2.136 2.939v5.669H9.351V9h3.413v1.561h.049c.476-.9 1.637-1.852 3.372-1.852 3.604 0 4.268 2.373 4.268 5.459v6.284zM5.337 7.433a2.066 2.066 0 1 1 0-4.132 2.066 2.066 0 0 1 0 4.132zm1.777 13.019H3.559V9h3.555v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.727v20.545C0 23.226.792 24 1.771 24h20.451C23.2 24 24 23.226 24 22.272V1.727C24 .774 23.2 0 22.225 0z"/></svg>
                        </a>
                        {% endif %}
                        {% if profile.instagram %}
                        <a href="{{ profile.instagram }}" target="_blank" aria-label="Instagram">
                            <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 1.17.054 1.97.24 2.43.403a4.92 4.92 0 0 1 1.72 1.088 4.92 4.92 0 0 1 1.088 1.72c.163.46.35 1.26.403 2.43.058 1.266.07 1.646.07 4.85s-.012 3.584-.07 4.85c-.054 1.17-.24 1.97-.403 2.43a4.92 4.92 0 0 1-1.088 1.72 4.92 4.92 0 0 1-1.72 1.088c-.46.163-1.26.35-2.43.403-1.266.058-1.646.07-4.85.07s-3.584-.012-4.85-.07c-1.17-.054-1.97-.24-2.43-.403a4.92 4.92 0 0 1-1.72-1.088 4.92 4.92 0 0 1-1.088-1.72c-.163-.46-.35-1.26-.403-2.43C2.175 15.747 2.163 15.367 2.163 12s.012-3.584.07-4.85c.054-1.17.24-1.97.403-2.43a4.92 4.92 0 0 1 1.088-1.72 4.92 4.92 0 0 1 1.72-1.088c.46-.163 1.26-.35 2.43-.403C8.416 2.175 8.796 2.163 12 2.163zm0-2.163C8.741 0 8.332.013 7.052.072 5.78.13 4.842.31 4.042.652a6.978 6.978 0 0 0-2.53 1.64A6.978 6.978 0 0 0 .652 4.042C.31 4.842.13 5.78.072 7.052.013 8.332 0 8.741 0 12c0 3.259.013 3.668.072 4.948.058 1.272.238 2.21.58 3.01a6.978 6.978 0 0 0 1.64 2.53 6.978 6.978 0 0 0 2.53 1.64c.8.342 1.738.522 3.01.58C8.332 23.987 8.741 24 12 24s3.668-.013 4.948-.072c1.272-.058 2.21-.238 3.01-.58a6.978 6.978 0 0 0 2.53-1.64 6.978 6.978 0 0 0 1.64-2.53c.342-.8.522-1.738.58-3.01.059-1.28.072-1.689.072-4.948s-.013-3.668-.072-4.948c-.058-1.272-.238-2.21-.58-3.01a6.978 6.978 0 0 0-1.64-2.53A6.978 6.978 0 0 0 19.958.652C19.158.31 18.22.13 16.948.072 15.668.013 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zm0 10.162a3.999 3.999 0 1 1 0-7.998 3.999 3.999 0 0 1 0 7.998zm6.406-11.845a1.44 1.44 0 1 1-2.881 0 1.44 1.44 0 0 1 2.881 0z"/></svg>
                        </a>
                        {% endif %}
                    </div>
                </div>
                <form method="post" class="contact-form">
                    {% csrf_token %}
                    <div class="field-group">
                        <label class="field-label">Name</label>
                        <input name="name" placeholder="Your name" required>
                    </div>
                    <div class="field-group">
                        <label class="field-label">Email</label>
                        <input name="email" type="email" placeholder="your@email.com" required>
                    </div>
                    <div class="field-group">
                        <label class="field-label">Phone <span style="opacity:.4">\u2014 optional</span></label>
                        <input name="phone" placeholder="+91 ...">
                    </div>
                    <div class="field-group">
                        <label class="field-label">Message</label>
                        <textarea name="message" placeholder="What are we working on?"></textarea>
                    </div>
                    <button type="submit" class="form-submit">Send Message \u2192</button>
                </form>
            </div>
        </section>

        <footer class="footer">
            <div class="footer-watermark">{{ profile.name|upper }}</div>
            <div class="footer-bottom">
                <div class="footer-credit">Designed &amp; built by <strong>{{ profile.name }}</strong></div>
                <div class="footer-visits">V{{ visits }}.io</div>
            </div>
        </footer>

    </main>
</div>

<div class="overlay" id="overlay" onclick="togglePanel()"></div>
<div class="panel" id="panel">
    <button class="panel-close" onclick="togglePanel()">\u2715</button>
    <div class="panel-header">
        <div class="panel-label">Contact</div>
        <h3>Let's build<br>something.</h3>
    </div>
    <form method="post">
        {% csrf_token %}
        <div class="field-group">
            <label class="field-label">NAME</label>
            <input name="name" placeholder="Your name" required>
        </div>
        <div class="field-group">
            <label class="field-label">EMAIL</label>
            <input name="email" type="email" placeholder="your@email.com" required>
        </div>
        <div class="field-group">
            <label class="field-label">PHONE <span style="opacity:.4">\u2014 optional</span></label>
            <input name="phone" placeholder="+91 ...">
        </div>
        <div class="field-group">
            <label class="field-label">MESSAGE</label>
            <textarea name="message" placeholder="What are we working on?"></textarea>
        </div>
        <button type="submit" class="panel-submit">SEND MESSAGE \u2192</button>
    </form>
</div>

<div class="sb-email-toast" id="emailToast">Email copied!</div>

<script>
    function togglePanel() {
        document.getElementById('panel').classList.toggle('show');
        document.getElementById('overlay').classList.toggle('show');
    }

    function filterPosts(type, btn) {
        document.querySelectorAll('.post').forEach(p => {
            const show = type === 'all' || p.dataset.type === type;
            p.style.display = show ? '' : 'none';
            if (show) {
                p.style.animation = 'none';
                p.offsetHeight;
                p.style.animation = 'fadeUp .45s cubic-bezier(.22,1,.36,1) forwards';
            }
        });
        document.querySelectorAll('.filters button').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
    }

    function toggleMobileMenu() {
        document.getElementById('mobileMenu').classList.toggle('show');
    }

    function copyEmail() {
        const email = document.getElementById('emailText').textContent;
        navigator.clipboard.writeText(email).then(() => {
            const toast = document.getElementById('emailToast');
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        });
    }

    function updateActiveNav() {
        const sections = ['hero', 'projects', 'skills', 'contact'];
        const navItems = document.querySelectorAll('.sb-nav-item');
        let current = 'hero';
        sections.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                const rect = el.getBoundingClientRect();
                if (rect.top <= 200) current = id;
            }
        });
        navItems.forEach(item => {
            item.classList.toggle('active', item.dataset.nav === current);
        });
    }

    window.addEventListener('scroll', updateActiveNav, { passive: true });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.anim-fade-up, .skill-card, .post').forEach(el => {
        observer.observe(el);
    });
</script>

</body>
</html>
"""

TARGET.write_text(HTML, encoding="utf-8")
print(f"Written {len(HTML)} bytes to {TARGET}")
print(f"Lines: {len(HTML.splitlines())}")

