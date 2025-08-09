const API_BASE = "http://localhost:8000";

function getCurrentUserId() {
  const user = JSON.parse(localStorage.getItem('currentUser') || '{}');
  return user.id || null;
}

export async function fetchGroups() {
  try {
    const response = await fetch(`${API_BASE}/groups`);
    if (!response.ok) throw new Error("Failed to fetch groups");
    return await response.json();
  } catch {
    return [];
  }
}

export async function fetchUnits() {
  try {
    const response = await fetch(`${API_BASE}/units`);
    if (!response.ok) throw new Error("Failed to fetch units");
    return await response.json();
  } catch {
    return [];
  }
}

export async function fetchStudentsLookingForTeam(unitCode = null) {
  try {
    const response = await fetch(`${API_BASE}/team-posts/looking-for-team`);
    if (!response.ok) throw new Error("Failed to fetch team posts");
    const teamPosts = await response.json();
    if (unitCode) {
      return teamPosts.filter((post) => post.unit_code === unitCode);
    }
    return teamPosts;
  } catch {
    return [];
  }
}

export async function fetchEnrolments() {
  try {
    const response = await fetch(`${API_BASE}/enrolments`);
    if (!response.ok) throw new Error("Failed to fetch enrolments");
    return await response.json();
  } catch {
    return [];
  }
}

export async function createTeamPost(studentId, unitCode, lookingForTeam, openToMessages, note) {
  try {
    const response = await fetch(`${API_BASE}/team-posts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: studentId,
        unit_code: unitCode,
        looking_for_team: lookingForTeam,
        open_to_messages: openToMessages,
        note: note,
      }),
    });
    if (!response.ok) throw new Error("Failed to create team post");
    return await response.json();
  } catch {
    return null;
  }
}

export async function fetchTeamPosts() {
  try {
    const response = await fetch(`${API_BASE}/team-posts/looking-for-team`);
    if (!response.ok) throw new Error("Failed to fetch team posts");
    return await response.json();
  } catch {
    return [];
  }
}

export async function enrollInUnit(unitCode) {
  try {
    const userId = getCurrentUserId();
    if (!userId) throw new Error("User not authenticated");
    
    const response = await fetch(`${API_BASE}/enrolments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        unit_code: unitCode,
        student_id: userId,
        grade: 0.0,
        completed: false,
        availability: "",
      }),
    });
    if (!response.ok) throw new Error("Failed to enroll in unit");
    return await response.json();
  } catch {
    return null;
  }
}

export async function fetchAvailableUnits(studentId = null) {
  try {
    const userId = studentId || getCurrentUserId();
    if (!userId) throw new Error("User not authenticated");
    
    const [allUnits, studentEnrolments] = await Promise.all([
      fetchUnits(),
      fetch(`${API_BASE}/students/${userId}/enrolments`).then((r) => r.json()).catch(() => []),
    ]);

    const enrolledCodes = new Set(studentEnrolments.map((e) => e.unit_code));
    return allUnits.filter((unit) => !enrolledCodes.has(unit.code));
  } catch {
    return [];
  }
}

export async function fetchMyGroups(studentId = null) {
  try {
    const userId = studentId || getCurrentUserId();
    if (!userId) throw new Error("User not authenticated");
    
    const [allGroups, allMembers] = await Promise.all([
      fetch(`${API_BASE}/groups`).then((r) => r.json()),
      fetch(`${API_BASE}/group-requests`).then((r) => r.json()).catch(() => []),
    ]);

    return allGroups.slice(0, 2);
  } catch {
    return [];
  }
}

export async function fetchGroupRequests(studentId = null) {
  try {
    const userId = studentId || getCurrentUserId();
    if (!userId) throw new Error("User not authenticated");
    
    const response = await fetch(`${API_BASE}/students/${userId}/group-requests`);
    if (!response.ok) throw new Error("Failed to fetch group requests");
    return await response.json();
  } catch {
    return [];
  }
}

export async function fetchGroupDetails(groupId) {
  try {
    const response = await fetch(`${API_BASE}/groups`);
    if (!response.ok) throw new Error("Failed to fetch group details");
    const groups = await response.json();

    let group = null;
    if (groupId.includes("-")) {
      const [unit_code, num, id] = groupId.split("-");
      group = groups.find((g) => g.unit_code === unit_code && String(g.num) === num && String(g.id) === id);
    } else {
      group = groups.find((g) => String(g.id) === String(groupId));
    }

    if (!group) throw new Error("Group not found");

    return {
      ...group,
      members: [
        { student_id: 1, name: "You", avatar: "https://cdn.discordapp.com/embed/avatars/0.png", availability: "Mon-Wed 2-6pm, Fri 10am-2pm" },
        { student_id: 2, name: "Alice Johnson", avatar: "https://cdn.discordapp.com/embed/avatars/0.png", availability: "Tue-Thu 1-5pm, Sat 9am-1pm" },
        { student_id: 3, name: "Bob Smith", avatar: "https://cdn.discordapp.com/embed/avatars/1.png", availability: "Mon-Fri 3-7pm" },
      ],
      messages: [
        { id: 1, from: "Alice Johnson", text: "Hey team, when can we meet?" },
        { id: 2, from: "You", text: "Tomorrow 2pm works for me." },
        { id: 3, from: "Bob Smith", text: "Same here!" },
      ],
      incoming_requests: [
        { student_id: 4, name: "Charlie Brown", avatar: "https://cdn.discordapp.com/embed/avatars/2.png", availability: "Weekends 10am-4pm" },
        { student_id: 5, name: "Diana Prince", avatar: "https://cdn.discordapp.com/embed/avatars/3.png", availability: "Mon-Wed evenings" },
      ],
    };
  } catch {
    return null;
  }
}

export async function createGroupRequest(groupId, studentId = null) {
  try {
    const userId = studentId || getCurrentUserId();
    if (!userId) throw new Error("User not authenticated");
    
    const response = await fetch(`${API_BASE}/group-requests`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ group_id: groupId, student_id: userId }),
    });
    if (!response.ok) throw new Error("Failed to create group request");
    return await response.json();
  } catch {
    return null;
  }
}

export async function deleteGroupRequest(groupId, studentId = null) {
  try {
    const userId = studentId || getCurrentUserId();
    if (!userId) throw new Error("User not authenticated");
    
    const response = await fetch(`${API_BASE}/group-requests/${groupId}/${userId}`, { method: "DELETE" });
    if (!response.ok) throw new Error("Failed to delete group request");
    return await response.json();
  } catch {
    return null;
  }
}

export async function fetchAssessments() {
  try {
    const response = await fetch(`${API_BASE}/assessments`);
    if (!response.ok) throw new Error("Failed to fetch assessments");
    return await response.json();
  } catch {
    return [];
  }
}

export async function fetchUnitAssessments(unitCode) {
  try {
    const response = await fetch(`${API_BASE}/units/${unitCode}/assessments`);
    if (!response.ok) throw new Error("Failed to fetch unit assessments");
    return await response.json();
  } catch {
    return [];
  }
}

export async function fetchAssessmentGroups(unitCode, assessmentNum) {
  try {
    const response = await fetch(`${API_BASE}/units/${unitCode}/assessments/${assessmentNum}/groups`);
    if (!response.ok) throw new Error("Failed to fetch assessment groups");
    return await response.json();
  } catch {
    return [];
  }
}

export async function authenticateUser(username, password) {
  try {
    const response = await fetch(`${API_BASE}/auth`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!response.ok) throw new Error(`Authentication failed: ${response.status}`);
    return await response.json();
  } catch {
    return { success: false, message: "Authentication failed" };
  }
}