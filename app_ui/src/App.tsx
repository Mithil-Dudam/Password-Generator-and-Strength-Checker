import { FormEvent, useState } from 'react'
import './App.css'
import api from './api'

function App() {
  const [display, setDisplay] = useState<number>(0)
  const [length, setLength] = useState<number>(0)
  const [uppercaseLetters,setUppercaseLetters] = useState<boolean>(false)
  const [numbers,setNumbers] = useState<boolean>(false)
  const [symbols,setSymbols] = useState<boolean>(false)
  const [password,setPassword] = useState<string>("")
  const [error,setError] = useState<string|null>(null)
  const [result,setResult] = useState<string>("")
  const [lowercaseCount,setLowercaseCount] = useState<number>(0)
  const [uppercaseCount,setUppercaseCount] = useState<number>(0)
  const [numberCount,setNumberCount] = useState<number>(0)
  const [symbolCount,setSymbolCount] = useState<number>(0)

  const Generate = async (e:FormEvent) => {
    setError(null)
    e.preventDefault()

    if(length===0){
      setError("Enter a length for the password")
      return
    }

    try{
      const response = await api.post("/generate",{length:length,upper:uppercaseLetters,number:numbers,symbol:symbols})
      if(response.status===200){
        setPassword(response.data.password)
      }
    }catch(error:any){
      console.error(error)
      setError("Error: Couldnt generate password")
    }
  }

  const Check = async () =>{
    setError(null)
    setDisplay(1)

    if(password===""){
      setError("Cant enter empty password")
      return
    }

    try{
      const response = await api.post("/check",{password:password})
      if(response.status===200){
        setResult(response.data.result)
        setLowercaseCount(response.data.lowercase)
        setUppercaseCount(response.data.uppercase)
        setNumberCount(response.data.numbers)
        setSymbolCount(response.data.symbols)
      }
    }catch(error:any){
      console.error(error)
      setError("Error: Couldnt check strength of password")
    }
  }

  return (
    <div className='bg-black text-yellow-300 min-w-screen min-h-screen'>
      <div>
        <h1 className='text-center pt-10 text-6xl'>Password Generator & Strength Checker</h1>
      </div>
      <div className='flex justify-between mt-10 px-5 mx-5'>
        <button onClick={()=>setDisplay(0)} className={`border w-full mr-5 cursor-pointer hover:bg-yellow-300 hover:text-black py-1 text-xl font-semibold ${display === 0 ? "bg-yellow-300 text-black":""}`}>Password Generator</button>
        <button onClick={()=>setDisplay(1)} className={`border w-full mr-5 cursor-pointer hover:bg-yellow-300 hover:text-black py-1 text-xl font-semibold ${display === 1 ? "bg-yellow-300 text-black":""}`}>Strength Checker</button>
      </div>
      {display===0 && (
        <div className='mt-10 pl-5 text-2xl flex w-full'>
          <form className='border w-[50%] px-5 pt-5' onSubmit={Generate}>
            <div className='flex justify-between my-2'>
              <label className='mr-5'>Enter Length of Password to be generated: </label>
              <input type='number' className='text-white w-[60px] pl-1 border-yellow-300 ring ring-white rounded' min={1} max={100} onChange={(e)=>setLength(Number(e.currentTarget.value))}/>
            </div>
            <div className='flex justify-between my-2'>
              <label className='mr-5'>Include UpperCase Letters ?</label>
              <input type='checkbox' checked={uppercaseLetters} className='cursor-pointer' onChange={(e)=>setUppercaseLetters(e.target.checked)}/>
            </div>
            <div className='flex justify-between my-2'> 
              <label className='mr-5'>Include Numbers ?</label>
              <input type='checkbox' checked={numbers} className='cursor-pointer' onChange={(e)=>setNumbers(e.target.checked)}/>
            </div>
            <div className='flex justify-between my-2'>
              <label className='mr-5 text-left'>Include Symbols ?</label>
              <input type='checkbox' checked={symbols} className='cursor-pointer' onChange={(e)=>setSymbols(e.target.checked)}/>
            </div>
            <div className='mt-3 mb-7 flex justify-center'>
              <button type="submit" className='border px-2 py-1 rounded cursor-pointer hover:bg-yellow-300 hover:text-black font-semibold'>Generate Password</button>
            </div>
          </form>
          <div className='flex flex-col w-[50%] border mx-5'>
            <div className='px-5 pt-5'>
              <h1>The generated password is:</h1>
              <p className={`break-all h-[50px] ${error ? "text-red-500":"text-white"}`}>{error ? error:password}</p>
            </div>
            <div className='mt-auto mb-7   flex ml-5 justify-center'>
                <button type="submit" onClick={Check} className='border px-2 py-1 rounded cursor-pointer hover:bg-yellow-300 hover:text-black font-semibold'>Check Strength</button>
            </div>
          </div>
        </div>
      )}
      {display===1 &&(
        <div className='mt-10 mx-5 border px-5 text-2xl'>
          <div className='flex flex-col'>
            <label className='mt-5'>Enter password:</label>
            <input type='text' className='text-white px-2 mx-2 ring ring-white' onChange={(e)=>setPassword(e.target.value)}/>
          </div>
          <div className='mt-10 mb-5 flex ml-5 justify-center'>
                <button onClick={Check} className='border px-2 py-1 rounded cursor-pointer hover:bg-yellow-300 hover:text-black font-semibold'>Check Strength</button>
            </div>
          <div>
            <h1>Password Strength:</h1>
            <p className={`h-[50px] ${error ? "text-red-500":"text-white"}`}>{error ? error:result}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
