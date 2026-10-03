import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {title:"CampusOS | Campus Intelligence",description:"A secure campus management and intelligence workspace.",icons:{icon:"/favicon.svg"},openGraph:{title:"CampusOS",description:"Campus intelligence, connected.",images:["/og.png"]},twitter:{card:"summary_large_image",title:"CampusOS",description:"Campus intelligence, connected.",images:["/og.png"]}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
