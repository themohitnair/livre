import { Card, CardContent } from "@/components/ui/card";

export default async function Home() {
  const res = await fetch('http://localhost:8000/');
  
  const data = await res.json();

  return (
    <div className="h-screen w-full flex items-center justify-center">
      <Card className="pt-7">
        <CardContent>
        <div className="sat flex flex-col items-center justify-center gap-5">
          <div className="wrap flex items-center justify-center gap-5">
            <div className="icon">
              <img src="/favicon/livre.svg" alt="Livre icon" className="w-32" />
            </div>
            <div className="server-name text-7xl">
              {data.title}
            </div>
          </div>
          <div className="subtitle text-xl">
            {data.subtitle}
          </div>        
        </div>
        </CardContent>
      </Card>
    </div>
  );
}