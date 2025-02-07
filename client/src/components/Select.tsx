import * as React from "react"
import Image from "next/image"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

export function SelectScrollable() {
  return (
    <Select>

      <SelectTrigger className="w-[100%]">
        <Image src="/logoWithWhite.png" className="mr-4 spin" alt="Logo" width={20} height={20}/>
        <SelectValue placeholder="XENO AI" />
      </SelectTrigger>
      
    </Select>
  )
}
