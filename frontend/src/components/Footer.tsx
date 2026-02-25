import { FaLinkedin } from "react-icons/fa";
import { FaGithub } from "react-icons/fa";


const Footer = () => {
    return (
        <footer className="border-t border-gray-800 mt-auto">
            <div className="max-w-7xl mx-auto px-4 py-6">
                <div className="flex justify-center items-center text-3xl mb-2 space-x-4">
                    <a href="https://www.linkedin.com/in/isaiahflagerhearan/" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                    <FaLinkedin />
                    </a>
                    <a href="https://github.com/PapaZay" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                    <FaGithub/>
                    </a>
                </div>
                <div className="text-center text-sm text-gray-500">
                    © 2026 Polywatch. Built by Isaiah Flager-Hearan
                </div>
            </div>

        </footer>
    )
}

export default Footer;