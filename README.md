# TSU-UPSKILL

{
  "entities": {
    "UserProfile": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "UserProfile",
      "type": "object",
      "description": "Represents a user profile within the TSU Connect application.",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the UserProfile entity."
        },
        "studentId": {
          "type": "string",
          "description": "The student's ID number."
        },
        "email": {
          "type": "string",
          "description": "The user's @tsu.ac.th email address.",
          "format": "email"
        },
        "profilePictureUrl": {
          "type": "string",
          "description": "URL of the user's profile picture.",
          "format": "uri"
        },
        "role": {
          "type": "string",
          "description": "The user's role.",
          "enum": [
            "user",
            "admin"
          ]
        },
        "friendIds": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "An array of UIDs of users who are friends."
        }
      },
      "required": [
        "id",
        "studentId",
        "email",
        "role"
      ]
    },
    "DiscussionRoom": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "DiscussionRoom",
      "type": "object",
      "description": "Represents a discussion room within the TSU Connect application.",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the DiscussionRoom entity."
        },
        "name": {
          "type": "string",
          "description": "The name of the discussion room (e.g., Academic Inquiries)."
        },
        "description": {
          "type": "string",
          "description": "A description of the discussion room's purpose."
        }
      },
      "required": [
        "id",
        "name"
      ]
    },
    "Message": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "Message",
      "type": "object",
      "description": "Represents a message posted in a discussion room.",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the Message entity."
        },
        "roomId": {
          "type": "string",
          "description": "Reference to DiscussionRoom."
        },
        "authorId": {
          "type": "string",
          "description": "Reference to UserProfile. (Relationship: UserProfile 1:N Message)"
        },
        "content": {
          "type": "string",
          "description": "The content of the message."
        },
        "timestamp": {
          "type": "string",
          "description": "The timestamp of when the message was sent.",
          "format": "date-time"
        }
      },
      "required": [
        "id",
        "roomId",
        "authorId",
        "content",
        "timestamp"
      ]
    },
    "AdminPasswordResetRequest": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "AdminPasswordResetRequest",
      "type": "object",
      "description": "Represents an admin's request to reset a user's password.",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the AdminPasswordResetRequest entity."
        },
        "userEmail": {
          "type": "string",
          "description": "The email address of the user requesting a password reset.",
          "format": "email"
        },
        "requestTimestamp": {
          "type": "string",
          "description": "The timestamp of when the password reset was requested.",
          "format": "date-time"
        },
        "adminId": {
          "type": "string",
          "description": "Reference to UserProfile. (Relationship: UserProfile 1:N AdminPasswordResetRequest).  The admin handling this request."
        }
      },
      "required": [
        "id",
        "userEmail",
        "requestTimestamp"
      ]
    },
    "AccountDeletionRequest": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "AccountDeletionRequest",
      "type": "object",
      "description": "Represents a user's request to delete their account.",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique identifier for the AccountDeletionRequest entity."
        },
        "userEmail": {
          "type": "string",
          "description": "The email address of the user requesting deletion.",
          "format": "email"
        },
        "studentId": {
          "type": "string",
          "description": "The student ID associated with the account."
        },
        "userId": {
          "type": "string",
          "description": "The Firebase Auth UID of the user requesting deletion."
        },
        "requestTimestamp": {
          "type": "string",
          "description": "The timestamp of when the deletion was requested.",
          "format": "date-time"
        }
      },
      "required": [
        "id",
        "userEmail",
        "userId",
        "requestTimestamp"
      ]
    },
     "FriendRequest": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "FriendRequest",
      "type": "object",
      "description": "Represents a friend request between two users.",
      "properties": {
        "id": {
            "type": "string",
            "description": "Unique identifier for the FriendRequest entity."
        },
        "senderId": {
            "type": "string",
            "description": "The UID of the user sending the request."
        },
        "receiverId": {
            "type": "string",
            "description": "The UID of the user receiving the request."
        },
        "status": {
            "type": "string",
            "description": "The status of the friend request.",
            "enum": ["pending", "accepted", "declined"]
        },
        "timestamp": {
            "type": "string",
            "description": "The timestamp of when the request was sent.",
            "format": "date-time"
        },
        "senderProfile": {
            "type": "object",
            "description": "Denormalized profile of the sender for easy display.",
            "properties": {
                "nickname": {"type": "string"},
                "avatarUrl": {"type": "string"}
            },
            "required": ["nickname", "avatarUrl"]
        }
      },
      "required": ["id", "senderId", "receiverId", "status", "timestamp"]
    },
    "ProfilePost": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "ProfilePost",
      "type": "object",
      "description": "Represents a message posted on a user's profile wall.",
      "properties": {
        "id": { "type": "string", "description": "Unique identifier for the post." },
        "profileUserId": { "type": "string", "description": "The UID of the user whose profile this post is on." },
        "authorId": { "type": "string", "description": "The UID of the user who wrote the post." },
        "authorInfo": {
          "type": "object",
          "description": "Denormalized data of the author for easy display.",
          "properties": {
            "nickname": { "type": "string" },
            "avatarUrl": { "type": "string" }
          },
          "required": ["nickname", "avatarUrl"]
        },
        "content": { "type": "string", "description": "The content of the post." },
        "timestamp": { "type": "string", "description": "The timestamp when the post was created.", "format": "date-time" }
      },
      "required": ["id", "profileUserId", "authorId", "authorInfo", "content", "timestamp"]
    }
  },
  "auth": {
    "providers": [
      "password",
      "anonymous"
    ]
  },
  "firestore": {
    "structure": [
      {
        "path": "/users/{userId}",
        "definition": {
          "entityName": "UserProfile",
          "schema": {
            "$ref": "#/backend/entities/UserProfile"
          },
          "description": "Stores user profile information. Path-based ownership enforced using {userId}. Includes studentId, email, and profilePictureUrl.",
          "params": [
            {
              "name": "userId",
              "description": "The unique identifier of the user."
            }
          ]
        }
      },
      {
        "path": "/users/{userId}/posts/{postId}",
        "definition": {
            "entityName": "ProfilePost",
            "schema": {
                "$ref": "#/backend/entities/ProfilePost"
            },
            "description": "Stores posts made on a user's profile wall.",
            "params": [
                {
                    "name": "userId",
                    "description": "The user whose profile the posts belong to."
                },
                {
                    "name": "postId",
                    "description": "The unique identifier of the post."
                }
            ]
        }
      },
      {
        "path": "/discussionRooms/{roomId}",
        "definition": {
          "entityName": "DiscussionRoom",
          "schema": {
            "$ref": "#/backend/entities/DiscussionRoom"
          },
          "description": "Stores discussion room information. Includes name and description.",
          "params": [
            {
              "name": "roomId",
              "description": "The unique identifier of the discussion room."
            }
          ]
        }
      },
      {
        "path": "/discussionRooms/{roomId}/messages/{messageId}",
        "definition": {
          "entityName": "Message",
          "schema": {
            "$ref": "#/backend/entities/Message"
          },
          "description": "Stores messages within a discussion room.  Includes roomId, authorId, content, and timestamp.",
          "params": [
            {
              "name": "roomId",
              "description": "The unique identifier of the discussion room."
            },
            {
              "name": "messageId",
              "description": "The unique identifier of the message."
            }
          ]
        }
      },
      {
        "path": "/adminPasswordResetRequests/{requestId}",
        "definition": {
          "entityName": "AdminPasswordResetRequest",
          "schema": {
            "$ref": "#/backend/entities/AdminPasswordResetRequest"
          },
          "description": "Stores admin password reset requests. Includes userEmail, requestTimestamp, and adminId.",
          "params": [
            {
              "name": "requestId",
              "description": "The unique identifier of the password reset request."
            }
          ]
        }
      },
      {
        "path": "/accountDeletionRequests/{requestId}",
        "definition": {
          "entityName": "AccountDeletionRequest",
          "schema": {
            "$ref": "#/backend/entities/AccountDeletionRequest"
          },
          "description": "Stores user requests for account deletion.",
          "params": [
            {
              "name": "requestId",
              "description": "The unique identifier of the deletion request."
            }
          ]
        }
      },
       {
        "path": "/friendRequests/{requestId}",
        "definition": {
          "entityName": "FriendRequest",
          "schema": {
            "$ref": "#/backend/entities/FriendRequest"
          },
          "description": "Stores friend requests sent between users.",
          "params": [
            {
              "name": "requestId",
              "description": "The unique identifier for the friend request."
            }
          ]
        }
      }
    ],
    "reasoning": "The Firestore structure is designed to support the TSU Connect application, focusing on user profiles, discussion rooms, messages, and admin password reset requests. It emphasizes authorization independence and simplified security rules through denormalization.\n\n*   **User Profiles:** Each user has a dedicated document under `/users/{userId}`. This path-based ownership allows straightforward security rules based on `request.auth.uid`. The profile picture URL is stored directly within the user profile.\n*   **Discussion Rooms:** Discussion rooms are stored in the `/discussionRooms` collection. \n*   **Messages:** Each discussion room has a subcollection `/discussionRooms/{roomId}/messages/{messageId}` to store messages. This nested hierarchical path simplifies data retrieval and security rules based on room membership.\n*   **Admin Password Reset Requests:** Admin password reset requests are stored in the `/adminPasswordResetRequests` collection.\n\n**Authorization Independence & QAPs:**\n\nAuthorization independence is achieved primarily through path-based ownership for user profiles. The use of subcollections for messages within discussion rooms allows messages to inherit security context from their parent room, simplifying rules. To further enhance this, if more complex room authorization were required, the `discussionRooms` documents could include a `members` map to store user roles within the room. The application implements QAPs by segregating data into collections with homogeneous security needs (e.g., private user profiles in `/users/{userId}`, public discussion rooms in `/discussionRooms`). This segregation makes it easy to define `list` operations based on the collection without needing complex filtering logic within the security rules. The admin password reset requests are stored in a separate collection `/adminPasswordResetRequests` which can be secured to allow only admins to access it."
    
"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LogOut, Settings, User as UserIcon, BookOpen, Building2, HeartHandshake, UserPlus, Check, X, Users, Mail } from "lucide-react";
import React, { useMemo } from "react";
import { signOut } from 'firebase/auth';
import { collection, query, where, orderBy, doc, getDoc, DocumentData, writeBatch, serverTimestamp, arrayUnion, getDocs, collectionGroup, setDoc } from 'firebase/firestore';


import { AppLogo } from "@/components/app-logo";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import {
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useAuth, useUser, useFirestore, useDoc, useCollection } from "@/firebase";
import { rooms } from "@/lib/data";
import type { Room, User, FriendRequest } from "@/lib/types";
import { useMemoFirebase } from "@/hooks/use-memo-firebase";
import { WithId } from "@/firebase/firestore/use-collection";
import { useToast } from "@/hooks/use-toast";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

const iconMap: Record<string, React.ElementType> = {
  BookOpen,
  Building2,
  HeartHandshake
};

export default function DashboardNav() {
  const pathname = usePathname();
  const router = useRouter();
  const auth = useAuth();
  const firestore = useFirestore();
  const { user: authUser, loading: isAuthLoading } = useUser();
  const { toast } = useToast();
  

  const userProfileRef = useMemoFirebase(() => {
    if (!firestore || !authUser) return null;
    return doc(firestore, "users", authUser.uid);
  }, [firestore, authUser]);

  const { data: userProfile, isLoading: isProfileLoading } = useDoc<User>(userProfileRef);

  const friendRequestsQuery = useMemoFirebase(() => {
    if (!firestore || !authUser) return null;
    return query(collection(firestore, "friendRequests"), where("receiverId", "==", authUser.uid), where("status", "==", "pending"));
  }, [firestore, authUser]);
  
  const { data: friendRequests, isLoading: friendRequestsLoading } = useCollection<FriendRequest>(friendRequestsQuery);

  const currentUser = useMemo(() => {
    if (isAuthLoading || isProfileLoading || !authUser || !userProfile) {
      return null;
    }
    return {
      id: authUser.uid,
      studentId: userProfile.studentId || 'N/A',
      email: authUser.email!,
      name: authUser.displayName || 'User',
      nickname: userProfile.nickname || authUser.displayName?.split(' ')[0] || 'User',
      avatarUrl: userProfile.profilePictureUrl || '',
      role: userProfile.role || 'user',
      friendIds: userProfile.friendIds || [],
    };
  }, [authUser, userProfile, isAuthLoading, isProfileLoading]);

  const handleLogout = async () => {
    if (!auth) return;
    await signOut(auth);
    router.push('/login');
  };

  const handleFriendRequest = async (request: WithId<FriendRequest>, action: 'accept' | 'decline') => {
      if (!firestore || !currentUser || !userProfile) return;
      
      const requestRef = doc(firestore, "friendRequests", request.id);
      const batch = writeBatch(firestore);

      if (action === 'accept') {
          const senderUserRef = doc(firestore, "users", request.senderId);
          const receiverUserRef = doc(firestore, "users", currentUser.id);

          // 1. Update friend lists for both users
          batch.update(senderUserRef, { 
              friendIds: arrayUnion(currentUser.id)
          });
          batch.update(receiverUserRef, { 
              friendIds: arrayUnion(request.senderId)
          });

          // 2. Mark the request as accepted
          batch.update(requestRef, { status: 'accepted' });

          try {
            await batch.commit();
            toast({
                title: "Friend Added!",
                description: `You are now friends with ${request.senderProfile.nickname}.`,
            });
          } catch (error) {
              console.error("Error accepting friend request:", error);
              toast({ variant: "destructive", title: "Error", description: "Could not process friend request."});
          }

      } else { // decline
          batch.update(requestRef, { status: 'declined' });
          try {
            await batch.commit();
            toast({
                title: "Request Declined",
                description: `You have declined ${request.senderProfile.nickname}'s friend request.`,
            });
          } catch (error) {
              console.error("Error declining friend request:", error);
              toast({ variant: "destructive", title: "Error", description: "Could not decline friend request."});
          }
      }
  }
  
  const getIcon = (iconName: string) => {
    const Icon = iconMap[iconName];
    return Icon ? <Icon /> : null;
  };
  
  if (isAuthLoading || isProfileLoading || !currentUser) {
    return (
        <>
            <SidebarHeader>
                <AppLogo />
            </SidebarHeader>
            <SidebarContent>
                {/* Skeleton Loading */}
            </SidebarContent>
            <SidebarFooter>
                 {/* Skeleton Loading */}
            </SidebarFooter>
        </>
    );
  }

  return (
    <>
      <SidebarHeader>
        <AppLogo />
      </SidebarHeader>
      <SidebarContent>
        {currentUser.role === 'admin' && (
           <SidebarGroup>
           <SidebarGroupLabel>Admin</SidebarGroupLabel>
           <SidebarMenu>
              <SidebarMenuItem>
                <Link href="/dashboard/admin" className="w-full">
                  <SidebarMenuButton
                    isActive={pathname === '/dashboard/admin'}
                    tooltip="Admin Inbox"
                  >
                    <Mail />
                    <span>Admin Inbox</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
           </SidebarMenu>
         </SidebarGroup>
        )}

        <SidebarGroup>
            <SidebarGroupLabel>Friend Requests</SidebarGroupLabel>
            <SidebarMenu>
              {friendRequestsLoading ? (
                <SidebarMenuItem><SidebarMenuButton>Loading requests...</SidebarMenuButton></SidebarMenuItem>
              ) : friendRequests && friendRequests.length > 0 ? (
                 friendRequests.map(req => (
                   <SidebarMenuItem key={req.id}>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger asChild>
                            <div className="flex w-full items-center gap-2 overflow-hidden rounded-md p-2 text-left text-sm">
                                <Avatar className="h-6 w-6">
                                    <AvatarImage src={req.senderProfile.avatarUrl} />
                                    <AvatarFallback>{req.senderProfile.nickname?.charAt(0)}</AvatarFallback>
                                </Avatar>
                                <span className="truncate flex-1">{req.senderProfile.nickname}</span>
                                <div className="flex gap-1">
                                    <Button size="icon" variant="ghost" className="h-6 w-6" onClick={() => handleFriendRequest(req, 'accept')}><Check className="h-4 w-4 text-green-500" /></Button>
                                    <Button size="icon" variant="ghost" className="h-6 w-6" onClick={() => handleFriendRequest(req, 'decline')}><X className="h-4 w-4 text-red-500" /></Button>
                                </div>
                            </div>
                        </TooltipTrigger>
                        <TooltipContent side="right">
                          <p>Friend request from {req.senderProfile.nickname}</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                   </SidebarMenuItem>
                 ))
              ) : (
                <p className="p-2 text-xs text-muted-foreground">No new friend requests.</p>
              )}
            </SidebarMenu>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Community</SidebarGroupLabel>
          <SidebarMenu>
             <SidebarMenuItem>
              <Link href="/dashboard/users" className="w-full">
                <SidebarMenuButton
                  isActive={pathname.startsWith('/dashboard/users')}
                  tooltip="Find Friends"
                >
                  <Users />
                  <span>Find Friends</span>
                </SidebarMenuButton>
              </Link>
            </SidebarMenuItem>
            {rooms.map((room: Room) => (
              <SidebarMenuItem key={room.id}>
                <Link href={`/dashboard/chat/${room.id}`} className="w-full">
                  <SidebarMenuButton
                    isActive={pathname.includes(`/dashboard/chat/${room.id}`)}
                    tooltip={room.name}
                  >
                    {getIcon(room.icon)}
                    <span>{room.name}</span>
                  </SidebarMenuButton>
                </Link>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroup>

      </SidebarContent>
      <SidebarFooter>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="w-full h-auto justify-start p-2">
              <div className="flex items-center gap-3 w-full">
                <Avatar className="h-9 w-9">
                  <AvatarImage src={currentUser.avatarUrl} alt={currentUser.name} />
                  <AvatarFallback>{currentUser.name.charAt(0)}</AvatarFallback>
                </Avatar>
                <div className="text-left hidden group-data-[state=expanded]:block">
                  <p className="font-medium text-sm text-sidebar-foreground truncate">{currentUser.nickname}</p>
                  <p className="text-xs text-muted-foreground truncate">{currentUser.email}</p>
                </div>
              </div>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56 mb-2" align="end" forceMount>
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium leading-none">{currentUser.name}</p>
                <p className="text-xs leading-none text-muted-foreground">
                  {currentUser.email}
                </p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <Link href="/dashboard/profile">
              <DropdownMenuItem>
                <UserIcon className="mr-2 h-4 w-4" />
                <span>My Profile</span>
              </DropdownMenuItem>
            </Link>
             <Link href="/dashboard/settings">
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" />
                <span>Settings</span>
              </DropdownMenuItem>
            </Link>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout}>
              <LogOut className="mr-2 h-4 w-4" />
              <span>Log out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarFooter>
    </>
  );
}

'use client';

import React, { useState, useMemo, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import {
  Camera,
  Mail,
  User as UserIcon,
  MessageSquare,
  Check,
  X,
  Edit,
  UserPlus,
  Clock,
  UserCheck,
  Send,
  Trash2,
} from 'lucide-react';
import {
  doc,
  updateDoc,
  collection,
  query,
  where,
  getDocs,
  addDoc,
  serverTimestamp,
  setDoc,
  getDoc,
  writeBatch,
  arrayUnion,
  limit,
  orderBy,
  deleteDoc,
} from 'firebase/firestore';
import { useRouter } from 'next/navigation';
import { updateProfile } from 'firebase/auth';
import { formatDistanceToNow } from 'date-fns';


import { PlaceHolderImages } from '@/lib/placeholder-images';
import { useAuth, useFirestore, useUser, useDoc, useCollection } from '@/firebase';
import { useMemoFirebase } from '@/hooks/use-memo-firebase';

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Separator } from '@/components/ui/separator';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/hooks/use-toast';
import { Skeleton } from '@/components/ui/skeleton';
import DashboardShell from './dashboard-shell';
import type { User, FriendRequest, ProfilePost } from '@/lib/types';


type UserProfileProps = {
  userId: string;
};

type FriendshipStatus = 'not_friends' | 'friends' | 'request_sent' | 'request_received';

const UserProfileContent: React.FC<UserProfileProps> = ({ userId }) => {
  const { user: authUser } = useUser();
  const firestore = useFirestore();
  const auth = useAuth();
  const router = useRouter();
  const { toast } = useToast();

  const isCurrentUserProfile = authUser?.uid === userId;

  const userProfileRef = useMemoFirebase(() => {
    if (!firestore || !userId) return null;
    return doc(firestore, 'users', userId);
  }, [firestore, userId]);
  
  const currentUserProfileRef = useMemoFirebase(() => {
    if (!firestore || !authUser) return null;
    return doc(firestore, 'users', authUser.uid);
  }, [firestore, authUser]);

  const profilePostsQuery = useMemoFirebase(() => {
    if (!firestore || !userId) return null;
    return query(collection(firestore, 'users', userId, 'posts'), orderBy('timestamp', 'desc'));
  }, [firestore, userId]);

  const { data: userProfile, isLoading: isProfileLoading } = useDoc<User>(userProfileRef);
  const { data: currentUserProfile, isLoading: isCurrentUserProfileLoading } = useDoc<User>(currentUserProfileRef);
  const { data: profilePosts, isLoading: isPostsLoading } = useCollection<ProfilePost>(profilePostsQuery);

  const [isAvatarDialogOpen, setIsAvatarDialogOpen] = useState(false);
  const [isEditingNickname, setIsEditingNickname] = useState(false);
  const [nickname, setNickname] = useState('');
  const [newPostContent, setNewPostContent] = useState("");
  
  const [friendshipStatus, setFriendshipStatus] = useState<FriendshipStatus>('not_friends');
  const [isFriendshipStatusLoading, setIsFriendshipStatusLoading] = useState(true);

  const displayedUser = useMemo(() => {
    if (!userProfile) return null;
    return {
      uid: userProfile.id,
      name: userProfile.name,
      nickname: userProfile.nickname,
      email: userProfile.email,
      studentId: userProfile.studentId,
      avatarUrl: userProfile.profilePictureUrl || '',
    };
  }, [userProfile]);

  useEffect(() => {
    if (displayedUser) {
      setNickname(displayedUser.nickname);
    }
  }, [displayedUser]);

  useEffect(() => {
    if (isCurrentUserProfile || !authUser || !userProfile || !currentUserProfile) {
        setIsFriendshipStatusLoading(false);
        return;
    }
    
    setIsFriendshipStatusLoading(true);

    // 1. Check if they are already friends
    if (currentUserProfile.friendIds?.includes(userProfile.id)) {
        setFriendshipStatus('friends');
        setIsFriendshipStatusLoading(false);
        return;
    }

    // 2. Check if there's a pending request
    const checkFriendRequest = async () => {
        if (!firestore) return;
        const requestsRef = collection(firestore, 'friendRequests');
        // Check if I sent a request to them
        const sentQuery = query(requestsRef, where('senderId', '==', authUser.uid), where('receiverId', '==', userProfile.id), where('status', '==', 'pending'), limit(1));
        const sentSnapshot = await getDocs(sentQuery);
        if (!sentSnapshot.empty) {
            setFriendshipStatus('request_sent');
            setIsFriendshipStatusLoading(false);
            return;
        }

        // Check if they sent a request to me
        const receivedQuery = query(requestsRef, where('senderId', '==', userProfile.id), where('receiverId', '==', authUser.uid), where('status', '==', 'pending'), limit(1));
        const receivedSnapshot = await getDocs(receivedQuery);
        if (!receivedSnapshot.empty) {
            setFriendshipStatus('request_received');
            setIsFriendshipStatusLoading(false);
            return;
        }
        
        setFriendshipStatus('not_friends');
        setIsFriendshipStatusLoading(false);
    }
    
    checkFriendRequest();

  }, [currentUserProfile, userProfile, authUser, isCurrentUserProfile, firestore]);

  const handleAvatarChange = async (imageUrl: string) => {
    if (!auth?.currentUser || !userProfileRef || !isCurrentUserProfile) return;
    try {
      await updateProfile(auth.currentUser, { photoURL: imageUrl });
      await updateDoc(userProfileRef, { profilePictureUrl: imageUrl });
      toast({ title: 'Avatar updated!' });
      setIsAvatarDialogOpen(false);
    } catch (error) {
      console.error('Error updating avatar:', error);
      toast({
        variant: 'destructive',
        title: 'Error',
        description: 'Could not update avatar.',
      });
    }
  };

  const handleNicknameSave = async () => {
    if (!userProfileRef || !auth?.currentUser || !isCurrentUserProfile) return;
    try {
      await updateDoc(userProfileRef, { nickname: nickname });
      await updateProfile(auth.currentUser, { displayName: nickname });
      setIsEditingNickname(false);
      toast({
        title: 'Nickname Updated!',
        description: 'Your new nickname has been saved.',
      });
    } catch (error) {
      console.error('Error updating nickname:', error);
      toast({
        variant: 'destructive',
        title: 'Error',
        description: 'Could not update nickname.',
      });
    }
  };

  const handleNicknameCancel = () => {
    if (displayedUser) {
      setNickname(displayedUser.nickname);
    }
    setIsEditingNickname(false);
  };

  const handleAddFriend = async () => {
      if (!firestore || !authUser || !displayedUser || !currentUserProfile) return;
      
      const payload: Omit<FriendRequest, 'id' | 'timestamp'> = {
        senderId: authUser.uid,
        receiverId: displayedUser.uid,
        status: 'pending',
        senderProfile: {
          nickname: currentUserProfile.nickname,
          avatarUrl: currentUserProfile.profilePictureUrl
        }
      };

      try {
        await addDoc(collection(firestore, 'friendRequests'), {
          ...payload,
          timestamp: serverTimestamp(),
        });
        setFriendshipStatus('request_sent');
        toast({ title: "Friend Request Sent!", description: `Your request to ${displayedUser.nickname} has been sent.`});
      } catch (error) {
          console.error("Error sending friend request:", error);
          toast({ variant: "destructive", title: "Error", description: "Could not send friend request."});
      }
  }

  const handlePostSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!firestore || !authUser || !currentUserProfile || !newPostContent.trim() || !userProfile) return;

    try {
        const postsCollectionRef = collection(firestore, 'users', userProfile.id, 'posts');
        const newPostRef = doc(postsCollectionRef);
        await setDoc(newPostRef, {
            id: newPostRef.id,
            profileUserId: userProfile.id,
            authorId: authUser.uid,
            authorInfo: {
                nickname: currentUserProfile.nickname,
                avatarUrl: currentUserProfile.profilePictureUrl,
            },
            content: newPostContent,
            timestamp: serverTimestamp(),
        });
        setNewPostContent('');
        toast({ title: "Post Successful!", description: "Your message has been posted." });
    } catch (error) {
        console.error("Error posting message:", error);
        toast({ variant: "destructive", title: "Error", description: "Could not post your message." });
    }
  };

  const handleDeletePost = async (postId: string) => {
    if (!firestore || !userProfile) return;
    try {
        const postRef = doc(firestore, 'users', userProfile.id, 'posts', postId);
        await deleteDoc(postRef);
        toast({ title: "Post Deleted" });
    } catch (error) {
        console.error("Error deleting post:", error);
        toast({ variant: "destructive", title: "Error", description: "Could not delete the post." });
    }
  };

  const renderActionButtons = () => {
    if (isCurrentUserProfile) return null;
    if (isFriendshipStatusLoading || isProfileLoading || isCurrentUserProfileLoading) {
      return (
          <div className="flex gap-2">
            <Skeleton className="h-10 w-28" />
          </div>
      );
    }
    
    switch(friendshipStatus) {
        case 'not_friends':
            return (
                <Button onClick={handleAddFriend}>
                    <UserPlus className="mr-2 h-4 w-4" />
                    Add Friend
                </Button>
            );
        case 'request_sent':
            return (
                <Button variant="outline" disabled>
                    <Clock className="mr-2 h-4 w-4" />
                    Request Sent
                </Button>
            );
        case 'request_received':
             return (
                <p className="text-sm text-muted-foreground p-2 rounded-md border">Please respond from the sidebar.</p>
            );
        case 'friends':
            return (
                 <Button>
                    <UserCheck className="mr-2 h-4 w-4" />
                    Friends
                 </Button>
            );
        default:
            return null;
    }
  }

  if (isProfileLoading || !displayedUser) {
    return <UserProfile.Skeleton />;
  }

  return (
    <DashboardShell>
      <div className="flex h-full items-center justify-center p-4 sm:p-8 bg-muted/40">
        <Card className="w-full max-w-2xl shadow-lg rounded-xl">
          <CardHeader className="p-0">
            <div className="relative h-40">
              <Image
                src="https://picsum.photos/seed/header/1000/200"
                alt="Profile banner"
                fill
                className="object-cover rounded-t-xl"
                data-ai-hint="abstract background"
              />
              <div className="absolute bottom-0 left-6 translate-y-1/2">
                <div className="relative group">
                  <Avatar className="h-28 w-28 border-4 border-background">
                    <AvatarImage
                      src={displayedUser.avatarUrl}
                      alt={displayedUser.name}
                    />
                    <AvatarFallback className="text-3xl">
                      {displayedUser.name?.charAt(0)}
                    </AvatarFallback>
                  </Avatar>
                  {isCurrentUserProfile && (
                    <Dialog open={isAvatarDialogOpen} onOpenChange={setIsAvatarDialogOpen}>
                      <DialogTrigger asChild>
                        <Button
                          variant="outline"
                          size="icon"
                          className="absolute inset-0 h-full w-full rounded-full bg-black/50 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <Camera className="h-6 w-6" />
                        </Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Choose Your Avatar</DialogTitle>
                        </DialogHeader>
                        <div className="grid grid-cols-3 gap-4 py-4">
                          {PlaceHolderImages.map((img) => (
                            <button
                              key={img.id}
                              onClick={() => handleAvatarChange(img.imageUrl)}
                              className="rounded-full overflow-hidden border-2 border-transparent hover:border-primary focus:border-primary focus:outline-none transition-all"
                            >
                              <Image
                                src={img.imageUrl}
                                alt={img.description}
                                width={100}
                                height={100}
                                data-ai-hint={img.imageHint}
                              />
                            </button>
                          ))}
                        </div>
                      </DialogContent>
                    </Dialog>
                  )}
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-20">
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-4">
                  {isCurrentUserProfile && isEditingNickname ? (
                    <div className="flex items-center gap-2 flex-grow">
                      <Input
                        value={nickname}
                        onChange={(e) => setNickname(e.target.value)}
                        className="text-3xl font-bold font-headline h-auto p-0 border-0 shadow-none focus-visible:ring-0"
                      />
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={handleNicknameSave}
                      >
                        <Check className="h-5 w-5 text-green-500" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={handleNicknameCancel}
                      >
                        <X className="h-5 w-5 text-red-500" />
                      </Button>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2">
                      <CardTitle className="text-3xl font-bold font-headline">
                        {displayedUser.nickname}
                      </CardTitle>
                      {isCurrentUserProfile && (
                        <Button
                          size="icon"
                          variant="ghost"
                          onClick={() => setIsEditingNickname(true)}
                        >
                          <Edit className="h-5 w-5" />
                        </Button>
                      )}
                    </div>
                  )}
                </div>
                <p className="text-sm text-muted-foreground">
                  {displayedUser.name}
                </p>
              </div>
              <div className="flex gap-2">
                {renderActionButtons()}
              </div>
            </div>
            <div className="mt-4 space-y-4 text-muted-foreground">
              <div className="flex items-center gap-3">
                <Mail className="h-5 w-5" />
                <span>{displayedUser.email}</span>
              </div>
              <div className="flex items-center gap-3">
                <UserIcon className="h-5 w-5" />
                <span>Student ID: {displayedUser.studentId}</span>
              </div>
            </div>
            <Separator className="my-6" />

            {/* Profile Wall Section */}
            <div>
              <h3 className="text-lg font-semibold mb-4">กระดานข้อความ</h3>
              
              {/* Post Input Form */}
              <form onSubmit={handlePostSubmit} className="flex flex-col gap-2 mb-6">
                  <Textarea
                      placeholder={`บอกอะไรบางอย่างกับ ${displayedUser.nickname}...`}
                      value={newPostContent}
                      onChange={(e) => setNewPostContent(e.target.value)}
                      rows={3}
                      disabled={isCurrentUserProfileLoading}
                  />
                  <div className="flex justify-end">
                      <Button type="submit" disabled={!newPostContent.trim() || isCurrentUserProfileLoading}>
                          <Send className="mr-2 h-4 w-4"/>
                          โพสต์
                      </Button>
                  </div>
              </form>

              {/* Posts List */}
              <div className="space-y-6">
                {isPostsLoading && (
                  <>
                    <Skeleton className="h-20 w-full" />
                    <Skeleton className="h-20 w-full" />
                  </>
                )}
                {!isPostsLoading && profilePosts && profilePosts.length > 0 ? (
                  profilePosts.map(post => (
                    <div key={post.id} className="flex gap-4">
                      <Link href={`/dashboard/profile/${post.authorId}`}>
                        <Avatar>
                          <AvatarImage src={post.authorInfo.avatarUrl} alt={post.authorInfo.nickname} />
                          <AvatarFallback>{post.authorInfo.nickname.charAt(0)}</AvatarFallback>
                        </Avatar>
                      </Link>
                      <div className="flex-1">
                        <div className="flex justify-between items-center">
                            <div>
                                <Link href={`/dashboard/profile/${post.authorId}`} className="font-semibold hover:underline">{post.authorInfo.nickname}</Link>
                                <p className="text-xs text-muted-foreground">
                                    {post.timestamp ? formatDistanceToNow(post.timestamp.toDate(), { addSuffix: true }) : ''}
                                </p>
                            </div>
                            {(post.authorId === authUser?.uid || isCurrentUserProfile) && (
                                <Button variant="ghost" size="icon" className="h-7 w-7" onClick={() => handleDeletePost(post.id)}>
                                    <Trash2 className="h-4 w-4" />
                                </Button>
                            )}
                        </div>
                        <p className="mt-1 text-sm text-foreground whitespace-pre-wrap">{post.content}</p>
                      </div>
                    </div>
                  ))
                ) : (
                  !isPostsLoading && <p className="text-sm text-muted-foreground text-center py-4">ยังไม่มีข้อความบนกระดาน</p>
                )}
              </div>
            </div>
            
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  );
};

const UserProfileSkeleton = () => {
    return (
        <DashboardShell>
        <div className="flex h-full items-center justify-center p-4 sm:p-8 bg-muted/40">
           <Card className="w-full max-w-2xl">
                <CardHeader className="p-0">
                    <div className="relative h-40">
                        <Skeleton className="h-full w-full rounded-t-xl" />
                         <div className="absolute bottom-0 left-6 translate-y-1/2">
                             <Skeleton className="h-28 w-28 rounded-full border-4 border-background" />
                         </div>
                    </div>
                </CardHeader>
                <CardContent className="pt-20">
                     <div className="flex justify-between items-start">
                        <div>
                            <Skeleton className="h-8 w-48 mb-2" />
                            <Skeleton className="h-4 w-56 mb-4" />
                        </div>
                        <Skeleton className="h-10 w-36" />
                     </div>
                     <div className="mt-4 space-y-4">
                        <Skeleton className="h-6 w-64" />
                        <Skeleton className="h-6 w-40" />
                     </div>
                     <Separator className="my-6" />
                     <div>
                        <Skeleton className="h-6 w-32 mb-4" />
                        <Skeleton className="h-24 w-full mb-6" />
                        <div className="space-y-4">
                           <Skeleton className="h-20 w-full" />
                           <Skeleton className="h-20 w-full" />
                        </div>
                     </div>
                </CardContent>
           </Card>
        </div>
      </DashboardShell>
    )
}

const UserProfile = Object.assign(UserProfileContent, {
  Skeleton: UserProfileSkeleton,
});

export default UserProfile;

import { Timestamp } from 'firebase/firestore';

export type User = {
  id: string;
  studentId: string;
  email: string;
  name: string;
  nickname: string;
  avatarUrl: string;
  profilePictureUrl: string;
  role: 'admin' | 'user';
  friendIds?: string[];
};

export type Room = {
  id: string;
  name: string;
  description: string;
  icon: string;
};

export type Message = {
  id: string;
  roomId: string; // Can be for public rooms or DMs
  authorId: string;
  text: string;
  timestamp: Timestamp | null; // Allow both for mock and firestore
  author?: {
    name: string;
    avatarUrl: string;
  };
};

export type PasswordResetRequest = {
  id: string;
  userId: string;
  userEmail: string;
  studentId: string;
  requestTimestamp: Timestamp;
};

export type AccountDeletionRequest = {
  id: string;
  userId: string;
  userEmail: string;
  studentId: string;
  requestTimestamp: Timestamp;
};

export type FriendRequest = {
    id: string;
    senderId: string;
    receiverId: string;
    status: 'pending' | 'accepted' | 'declined';
    timestamp: Timestamp;
    senderProfile: {
        nickname: string;
        avatarUrl: string;
    }
}

export type ProfilePost = {
  id: string;
  profileUserId: string;
  authorId: string;
  authorInfo: {
    nickname: string;
    avatarUrl: string;
  };
  content: string;
  timestamp: Timestamp;
};


/**
 * TSU Connect - Firestore Security Rules
 *
 * @mode Prototyping
 * @description These rules are designed for rapid development. They enforce strict
 *   authorization (who can access what) but remain flexible on data shapes
 *   to allow for easy iteration on the application's features.
 *
 */
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // ------------------------------------------------------------------------
    // Helper Functions
    // ------------------------------------------------------------------------

    function isSignedIn() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return isSignedIn() && request.auth.uid == userId;
    }
    
    function isAdmin() {
      // Safely check for admin role.
      // Use exists() to prevent errors if the user doc or role field doesn't exist.
      return isSignedIn() && exists(/databases/$(database)/documents/users/$(request.auth.uid)) &&
             get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
    
    function isParticipant(chatId) {
      return isSignedIn() && request.auth.uid in get(/databases/$(database)/documents/directMessages/$(chatId)).data.participants;
    }

    // ------------------------------------------------------------------------
    // User Profiles (/users/{userId})
    // ------------------------------------------------------------------------
    // กฎสำหรับข้อมูลส่วนตัวของผู้ใช้
    match /users/{userId} {
      // ใครก็ได้ที่ล็อกอินแล้ว สามารถดูโปรไฟล์ของคนอื่นได้
      allow get: if isSignedIn();
      // สามารถ list user ได้เพื่อค้นหาตอนจะส่ง mail
      allow list: if isSignedIn(); 
      // อนุญาตให้ผู้ใช้สร้างโปรไฟล์ของตัวเองเท่านั้น
      allow create: if isOwner(userId);
      // อนุญาตให้เจ้าของโปรไฟล์แก้ไขข้อมูลตัวเองได้
      // และอนุญาตให้คนอื่นมาอัปเดตรายชื่อเพื่อน (friendIds) ของเราได้
      allow update: if isOwner(userId) || 
                       (isSignedIn() && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['friendIds']));
      // ห้ามลบโปรไฟล์
      allow delete: if false;

      // กฎสำหรับโพสต์บนโปรไฟล์
      match /posts/{postId} {
        // ทุกคนที่ล็อกอินสามารถอ่านและสร้างโพสต์ได้
        allow get, list: if isSignedIn();
        allow create: if isSignedIn() && request.resource.data.authorId == request.auth.uid;
        // อนุญาตให้เจ้าของโพสต์ หรือเจ้าของโปรไฟล์ลบโพสต์ได้
        allow delete: if isSignedIn() && (isOwner(request.resource.data.authorId) || isOwner(userId));
        // ไม่อนุญาตให้อัปเดต
        allow update: if false;
      }
    }
    
    // ------------------------------------------------------------------------
    // Friend Requests (/friendRequests/{requestId})
    // ------------------------------------------------------------------------
    // กฎสำหรับคำขอเป็นเพื่อน
    match /friendRequests/{requestId} {
        // ใครก็ตามที่ล็อกอิน สามารถอ่านคำขอเป็นเพื่อนได้
        allow get, list: if isSignedIn();
        // อนุญาตให้สร้างคำขอได้ ก็ต่อเมื่อคนส่งคือตัวเอง
        allow create: if isSignedIn() && request.resource.data.senderId == request.auth.uid;
        // อนุญาตให้ผู้รับอัปเดต (เพื่อยอมรับ/ปฏิเสธ) หรือผู้ส่งอัปเดต (เพื่อยกเลิก)
        allow update: if isSignedIn() && (request.auth.uid == resource.data.receiverId || request.auth.uid == resource.data.senderId);
        // อนุญาตให้ผู้รับหรือผู้ส่งลบคำขอได้ (หลังจากจัดการเสร็จแล้ว)
        allow delete: if isSignedIn() && (request.auth.uid == resource.data.receiverId || request.auth.uid == resource.data.senderId);
    }

    // ------------------------------------------------------------------------
    // Discussion Rooms & Messages (/discussionRooms/{roomId}/...)
    // ------------------------------------------------------------------------
    // กฎสำหรับห้องสนทนากลุ่ม
    match /discussionRooms/{roomId} {
      // ทุกคนสามารถเข้ามาดูข้อมูลห้องและรายการข้อความได้
      allow get, list: if true;
      // เฉพาะแอดมินเท่านั้นที่สามารถสร้าง, แก้ไข, หรือลบห้องสนทนากลุ่มได้
      allow create, update, delete: if isAdmin();

      // กฎสำหรับข้อความในห้องสนทนากลุ่ม
      match /messages/{messageId} {
        // ทุกคนสามารถอ่านข้อความได้
        allow get, list: if true;
        // อนุญาตให้สร้างข้อความได้ ก็ต่อเมื่อคนเขียนคือตัวเอง
        allow create: if isSignedIn() && request.resource.data.authorId == request.auth.uid;
        // อนุญาตให้เจ้าของข้อความแก้ไขหรือลบข้อความของตัวเองได้
        allow update, delete: if isOwner(resource.data.authorId);
      }
    }

    // ------------------------------------------------------------------------
    // Admin Collections
    // ------------------------------------------------------------------------
    // กฎสำหรับส่วนของแอดมิน
    match /adminPasswordResetRequests/{requestId} {
      // เฉพาะแอดมินเท่านั้นที่มีสิทธิ์ทำทุกอย่างกับคำขอรีเซ็ตรหัสผ่าน
      allow get, list, create, update, delete: if isAdmin();
    }
    
    match /accountDeletionRequests/{requestId} {
      // แอดมินสามารถจัดการคำขอลบบัญชีได้
      allow get, list, update, delete: if isAdmin();
      // แต่ผู้ใช้ทุกคนสามารถสร้างคำขอลบบัญชีของตัวเองได้
      allow create: if isSignedIn() && request.resource.data.userId == request.auth.uid;
    }
    
  }
}


/**
 * TSU Connect - Firestore Security Rules
 *
 * @mode Prototyping
 * @description These rules are designed for rapid development. They enforce strict
 *   authorization (who can access what) but remain flexible on data shapes
 *   to allow for easy iteration on the application's features.
 *
 */
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // ------------------------------------------------------------------------
    // Helper Functions
    // ------------------------------------------------------------------------

    function isSignedIn() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return isSignedIn() && request.auth.uid == userId;
    }
    
    function isAdmin() {
      // Safely check for admin role.
      // Use exists() to prevent errors if the user doc or role field doesn't exist.
      return isSignedIn() && exists(/databases/$(database)/documents/users/$(request.auth.uid)) &&
             get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
    
    function isParticipant(chatId) {
      return isSignedIn() && request.auth.uid in get(/databases/$(database)/documents/directMessages/$(chatId)).data.participants;
    }

    // ------------------------------------------------------------------------
    // User Profiles (/users/{userId})
    // ------------------------------------------------------------------------
    // กฎสำหรับข้อมูลส่วนตัวของผู้ใช้
    match /users/{userId} {
      // ใครก็ได้ที่ล็อกอินแล้ว สามารถดูโปรไฟล์ของคนอื่นได้
      allow get: if isSignedIn();
      // สามารถ list user ได้เพื่อค้นหาตอนจะส่ง mail
      allow list: if isSignedIn(); 
      // อนุญาตให้ผู้ใช้สร้างโปรไฟล์ของตัวเองเท่านั้น
      allow create: if isOwner(userId);
      // อนุญาตให้เจ้าของโปรไฟล์แก้ไขข้อมูลตัวเองได้
      // และอนุญาตให้คนอื่นมาอัปเดตรายชื่อเพื่อน (friendIds) ของเราได้
      allow update: if isOwner(userId) || 
                       (isSignedIn() && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['friendIds']));
      // ห้ามลบโปรไฟล์
      allow delete: if false;

      // กฎสำหรับโพสต์บนโปรไฟล์
      match /posts/{postId} {
        // ทุกคนที่ล็อกอินสามารถอ่านและสร้างโพสต์ได้
        allow get, list: if isSignedIn();
        allow create: if isSignedIn() && request.resource.data.authorId == request.auth.uid;
        // อนุญาตให้เจ้าของโพสต์ หรือเจ้าของโปรไฟล์ลบโพสต์ได้
        allow delete: if isSignedIn() && (isOwner(request.resource.data.authorId) || isOwner(userId));
        // ไม่อนุญาตให้อัปเดต
        allow update: if false;
      }
    }
    
    // ------------------------------------------------------------------------
    // Friend Requests (/friendRequests/{requestId})
    // ------------------------------------------------------------------------
    // กฎสำหรับคำขอเป็นเพื่อน
    match /friendRequests/{requestId} {
        // ใครก็ตามที่ล็อกอิน สามารถอ่านคำขอเป็นเพื่อนได้
        allow get, list: if isSignedIn();
        // อนุญาตให้สร้างคำขอได้ ก็ต่อเมื่อคนส่งคือตัวเอง
        allow create: if isSignedIn() && request.resource.data.senderId == request.auth.uid;
        // อนุญาตให้ผู้รับอัปเดต (เพื่อยอมรับ/ปฏิเสธ) หรือผู้ส่งอัปเดต (เพื่อยกเลิก)
        allow update: if isSignedIn() && (request.auth.uid == resource.data.receiverId || request.auth.uid == resource.data.senderId);
        // อนุญาตให้ผู้รับหรือผู้ส่งลบคำขอได้ (หลังจากจัดการเสร็จแล้ว)
        allow delete: if isSignedIn() && (request.auth.uid == resource.data.receiverId || request.auth.uid == resource.data.senderId);
    }

    // ------------------------------------------------------------------------
    // Discussion Rooms & Messages (/discussionRooms/{roomId}/...)
    // ------------------------------------------------------------------------
    // กฎสำหรับห้องสนทนากลุ่ม
    match /discussionRooms/{roomId} {
      // ทุกคนสามารถเข้ามาดูข้อมูลห้องและรายการข้อความได้
      allow get, list: if true;
      // เฉพาะแอดมินเท่านั้นที่สามารถสร้าง, แก้ไข, หรือลบห้องสนทนากลุ่มได้
      allow create, update, delete: if isAdmin();

      // กฎสำหรับข้อความในห้องสนทนากลุ่ม
      match /messages/{messageId} {
        // ทุกคนสามารถอ่านข้อความได้
        allow get, list: if true;
        // อนุญาตให้สร้างข้อความได้ ก็ต่อเมื่อคนเขียนคือตัวเอง
        allow create: if isSignedIn() && request.resource.data.authorId == request.auth.uid;
        // อนุญาตให้เจ้าของข้อความแก้ไขหรือลบข้อความของตัวเองได้
        allow update, delete: if isOwner(resource.data.authorId);
      }
    }

    // ------------------------------------------------------------------------
    // Admin Collections
    // ------------------------------------------------------------------------
    // กฎสำหรับส่วนของแอดมิน
    match /adminPasswordResetRequests/{requestId} {
      // เฉพาะแอดมินเท่านั้นที่มีสิทธิ์ทำทุกอย่างกับคำขอรีเซ็ตรหัสผ่าน
      allow get, list, create, update, delete: if isAdmin();
    }
    
    match /accountDeletionRequests/{requestId} {
      // แอดมินสามารถจัดการคำขอลบบัญชีได้
      allow get, list, update, delete: if isAdmin();
      // แต่ผู้ใช้ทุกคนสามารถสร้างคำขอลบบัญชีของตัวเองได้
      allow create: if isSignedIn() && request.resource.data.userId == request.auth.uid;
    }
    
  }
}
}

    
