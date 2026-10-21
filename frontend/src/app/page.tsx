import ChatInterface from "@/components/ChatInterface";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-6 md:p-24">
      <div className="z-10 w-full max-w-5xl">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Docsage</h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Chat with your PDF documents powered by RAG
          </p>
        </div>
        <ChatInterface />
      </div>
    </main>
  );
}