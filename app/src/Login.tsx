import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";

const Login = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  const handleLogin = async () => {
    try {
      const response = await fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username,
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Login failed!");
      }

      const data = await response.json();
      setMessage("Login successful!");
      localStorage.setItem('access_token', data.access_token);
    } catch (error: unknown) {
      if (error instanceof Error) {
        setMessage("Login failed: " + error.message);
      } else {
        setMessage("An unknown error occurred.");
      }
    }
  };

  return (    
    <div className="flex justify-center items-center h-screen">
      <Card className="w-3/12">
        <CardHeader className="flex items-center justify-center">
          <CardTitle>Login</CardTitle>
        </CardHeader>
        <CardContent>
          <Input 
            placeholder="Username" 
            className="mb-3" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
          />
          <Input 
            type="password" 
            placeholder="Password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
          />
          {message && (
            <div className="mt-3 text-center text-red-500">{message}</div>
          )}
        </CardContent>
        <CardFooter className="w-full">
          <Button variant="default" className="w-full" onClick={handleLogin}>
            Submit
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default Login;