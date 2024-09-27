import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import { Input } from "@/components/ui/input"

import { Button } from "@/components/ui/button"

import { useState } from "react"

const Register = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  const handleRegister = async () => {
    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error("Registration failed!");
      }

      const data = await response.json();
      setMessage("Registration successful!");
    } catch (error: unknown) {
      if (error instanceof Error) {
        setMessage(error.message);
      } else {
        setMessage("An unknown error occurred.");
      }
    }
  };


  return (    
    <div className="flex justify-center items-center h-screen">
      <Card className="w-3/12">
        <CardHeader className="flex items-center justify-center">
          <CardTitle>Register</CardTitle>
        </CardHeader>
        <CardContent>
          <Input placeholder="Username" className="mb-3" value={username} onChange={(e) => {setUsername(e.target.value)}}/>
          <Input type="password" placeholder="Password" value={password} onChange={(e) => {setPassword(e.target.value)}}/>
          {message && (
            <div className="mt-3 text-center text-red-500">{message}</div>
          )}
        </CardContent>
        <CardFooter className="w-full">
          <Button variant="default" className="w-full" onClick={handleRegister}>Submit</Button>
        </CardFooter>
      </Card>
    </div>
  )
}

export default Register;