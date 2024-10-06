import "./globals.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <link rel="icon" href="/favicon/livre.svg" type="image/svg" />
      <body>
        {children}
      </body>
    </html>
  );
}
