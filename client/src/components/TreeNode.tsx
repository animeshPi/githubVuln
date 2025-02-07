import { FileCode, Folder } from "lucide-react";
import { useState } from "react";

export function Tree({ treeData }) {
  return (
    <ul className="pl-4 flex cursor-pointer flex-col justify-start items-start gap-2">
      {treeData.map((node) => {
        return (<TreeNode node={node} key={node.key} />)
        
      }
      )}
    </ul>
  );
}

export default function TreeNode({ node }) {
  const { children, label } = node;
  const hasChildren = children && children.length > 0;

  const [showChildren, setShowChildren] = useState(false);

  const handleClick = () => {
    setShowChildren(!showChildren);
  };

  if(node.children){
    return (

         <>
    
      <div onClick={hasChildren ? handleClick : null} className="flex gap-2 justify-center items-center ">
        <Folder className="w-[16px]" />
        <span className="text-xs">{label}</span>
      </div>
      {hasChildren && showChildren && (
        <div>
        <ul className="pl-4 text-xs flex flex-col gap-2">
          <Tree treeData={children} />
        </ul>
        </div>
      )}
    </>


    );
  }else{
    return (

        <>
   
     <div onClick={hasChildren ? handleClick : null} className="flex gap-2 justify-center items-center ">
       <FileCode className="w-[16px]" />
       <span className="text-xs">{label}</span>
     </div>
     {hasChildren && showChildren && (
       <div>
       <ul className="pl-2 text-xs flex flex-col gap-2">
         <Tree treeData={children} />
       </ul>
       </div>
     )}
   </>


   );s
  }
 
}
