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

export async function fetchStudents() {
  try {
    const response = await fetch(`${API_BASE}/students`);
    if (!response.ok) throw new Error("Failed to fetch students");
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

    const group = groups.find((g) => String(g.id) === String(groupId));
    if (!group) throw new Error("Group not found");

    return {
      ...group,
      members: [],
      messages: [],
      incoming_requests: [],
      max_members: 5
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

export async function createAssessmentGroup(unitCode, assessmentNum, name) {
  try {
    const response = await fetch(`${API_BASE}/units/${unitCode}/assessments/${assessmentNum}/groups`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });
    if (!response.ok) throw new Error('Failed to create group');
    return await response.json();
  } catch {
    return null;
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

// DB-backed membership helpers
export async function fetchMyDbGroups(studentId) {
  try {
    const r = await fetch(`${API_BASE}/students/${studentId}/groups`);
    if (!r.ok) throw new Error('Failed to fetch my groups');
    return await r.json();
  } catch {
    return [];
  }
}

export async function fetchGroupMembers(groupId) {
  try {
    const r = await fetch(`${API_BASE}/groups/${groupId}/members`);
    if (!r.ok) throw new Error('Failed to fetch group members');
    return await r.json();
  } catch {
    return [];
  }
}

export async function joinGroupMember(groupId, studentId) {
  try {
    const r = await fetch(`${API_BASE}/groups/${groupId}/members`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: studentId })
    });
    if (!r.ok) throw new Error('Failed to join group');
    return await r.json();
  } catch {
    return null;
  }
}

// Additional helper for student-specific enrolments
export async function fetchStudentEnrolments(studentId) {
  try {
    const response = await fetch(`${API_BASE}/students/${studentId}/enrolments`);
    if (!response.ok) throw new Error("Failed to fetch student enrolments");
    return await response.json();
  } catch {
    return [];
  }
}
