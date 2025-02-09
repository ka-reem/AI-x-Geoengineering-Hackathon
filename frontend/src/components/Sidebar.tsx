import Link from 'next/link';
import { HomeIcon, DocumentTextIcon } from '@heroicons/react/24/outline';

export default function Sidebar() {
  return (
    <div className="hidden md:flex flex-col w-64 bg-indigo-700 text-white">
      <div className="p-4 border-b border-indigo-600">
        <h1 className="text-lg font-semibold">Climate Dashboard</h1>
      </div>
      <nav className="mt-4 flex-1">
        <ul className="space-y-1 px-2">
          <li>
            <Link href="/" className="flex items-center px-4 py-2 text-sm rounded-md hover:bg-indigo-600">
              <HomeIcon className="h-5 w-5 mr-3" />
              Dashboard
            </Link>
          </li>
          <li>
            <Link href="/documentation" className="flex items-center px-4 py-2 text-sm rounded-md hover:bg-indigo-600">
              <DocumentTextIcon className="h-5 w-5 mr-3" />
              Documentation
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
