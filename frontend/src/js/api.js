const API_BASE = "http://localhost:8000";

export async function fetchGroups() {
  try {
    const response = await fetch(`${API_BASE}/groups`);
    if (!response.ok) throw new Error("Failed to fetch groups");
    return await response.json();
  } catch (error) {
    console.error("Error fetching groups:", error);
    return [];
  }
}

export async function fetchUnits() {
  try {
    const response = await fetch(`${API_BASE}/units`);
    if (!response.ok) throw new Error("Failed to fetch units");
    return await response.json();
  } catch (error) {
    console.error("Error fetching units:", error);
    return [];
  }
}

export async function fetchStudentsLookingForTeam(unitCode = null) {
  try {
    const response = await fetch(`${API_BASE}/team-posts/looking-for-team`);
    if (!response.ok) throw new Error("Failed to fetch team posts");
    const teamPosts = await response.json();

    // Filter by unit code if specified
    if (unitCode) {
      return teamPosts.filter((post) => post.unit_code === unitCode);
    }

    return teamPosts;
  } catch (error) {
    console.error("Error fetching students looking for team:", error);
    return [];
  }
}

export async function fetchEnrolments() {
  try {
    const response = await fetch(`${API_BASE}/enrolments`);
    if (!response.ok) throw new Error("Failed to fetch enrolments");
    return await response.json();
  } catch (error) {
    console.error("Error fetching enrolments:", error);
    return [];
  }
}

export async function createTeamPost(
  studentId,
  unitCode,
  lookingForTeam,
  openToMessages,
  note,
) {
  try {
    const response = await fetch(`${API_BASE}/team-posts`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
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
  } catch (error) {
    console.error("Error creating team post:", error);
    return null;
  }
}

export async function fetchTeamPosts() {
  try {
    const response = await fetch(`${API_BASE}/team-posts/looking-for-team`);
    if (!response.ok) throw new Error("Failed to fetch team posts");
    return await response.json();
  } catch (error) {
    console.error("Error fetching team posts:", error);
    return [];
  }
}

export async function enrollInUnit(unitCode) {
  try {
    const response = await fetch(`${API_BASE}/enrolments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        unit_code: unitCode,
        student_id: 1, // Mock current user ID
        grade: 0.0,
        completed: false,
        availability: "",
      }),
    });
    if (!response.ok) throw new Error("Failed to enroll in unit");
    return await response.json();
  } catch (error) {
    console.error("Error enrolling in unit:", error);
    return null;
  }
}

export async function fetchAvailableUnits(studentId = 1) {
  try {
    const [allUnits, studentEnrolments] = await Promise.all([
      fetchUnits(),
      fetch(`${API_BASE}/students/${studentId}/enrolments`)
        .then((r) => r.json())
        .catch(() => []),
    ]);

    const enrolledCodes = new Set(studentEnrolments.map((e) => e.unit_code));
    return allUnits.filter((unit) => !enrolledCodes.has(unit.code));
  } catch (error) {
    console.error("Error fetching available units:", error);
    return [];
  }
}

export async function fetchMyGroups(studentId = 1) {
  try {
    // Get all groups and group member data to find which groups this student is in
    const [allGroups, allMembers] = await Promise.all([
      fetch(`${API_BASE}/groups`).then((r) => r.json()),
      fetch(`${API_BASE}/group-requests`)
        .then((r) => r.json())
        .catch(() => []), // Get all group requests to find members
    ]);

    // For now, just return some groups as a mock since we don't have a direct endpoint
    // In a real app, you'd want a proper /students/{id}/groups endpoint
    return allGroups.slice(0, 2); // Return first 2 groups as mock "my groups"
  } catch (error) {
    console.error("Error fetching my groups:", error);
    return [];
  }
}

export async function fetchGroupRequests(studentId = 1) {
  try {
    const response = await fetch(
      `${API_BASE}/students/${studentId}/group-requests`,
    );
    if (!response.ok) throw new Error("Failed to fetch group requests");
    return await response.json();
  } catch (error) {
    console.error("Error fetching group requests:", error);
    return [];
  }
}

export async function fetchGroupDetails(groupId) {
  try {
    const response = await fetch(`${API_BASE}/groups`);
    if (!response.ok) throw new Error("Failed to fetch group details");
    const groups = await response.json();

    // Find the specific group - handle different ID formats
    let group = null;

    if (groupId.includes("-")) {
      // Handle "CAB302-1-1" format
      const [unit_code, num, id] = groupId.split("-");
      group = groups.find(
        (g) =>
          g.unit_code === unit_code &&
          String(g.num) === num &&
          String(g.id) === id,
      );
    } else {
      // Handle numeric ID
      group = groups.find((g) => String(g.id) === String(groupId));
    }

    if (!group) {
      throw new Error("Group not found");
    }

    // Mock additional details like members and messages since backend doesn't provide them yet
    return {
      ...group,
      members: [
        {
          student_id: 1,
          name: "You",
          avatar: "https://cdn.discordapp.com/embed/avatars/0.png",
          availability: "Mon-Wed 2-6pm, Fri 10am-2pm",
        },
        {
          student_id: 2,
          name: "Alice Johnson",
          avatar: "https://cdn.discordapp.com/embed/avatars/0.png",
          availability: "Tue-Thu 1-5pm, Sat 9am-1pm",
        },
        {
          student_id: 3,
          name: "Bob Smith",
          avatar: "https://cdn.discordapp.com/embed/avatars/1.png",
          availability: "Mon-Fri 3-7pm",
        },
      ],
      messages: [
        { id: 1, from: "Alice Johnson", text: "Hey team, when can we meet?" },
        { id: 2, from: "You", text: "Tomorrow 2pm works for me." },
        { id: 3, from: "Bob Smith", text: "Same here!" },
      ],
      incoming_requests: [
        {
          student_id: 4,
          name: "Charlie Brown",
          avatar: "https://cdn.discordapp.com/embed/avatars/2.png",
          availability: "Weekends 10am-4pm",
        },
        {
          student_id: 5,
          name: "Diana Prince",
          avatar: "https://cdn.discordapp.com/embed/avatars/3.png",
          availability: "Mon-Wed evenings",
        },
      ],
    };
  } catch (error) {
    console.error("Error fetching group details:", error);
    return null;
  }
}

export async function createGroupRequest(groupId, studentId = 1) {
  try {
    const response = await fetch(`${API_BASE}/group-requests`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        group_id: groupId,
        student_id: studentId,
      }),
    });
    if (!response.ok) throw new Error("Failed to create group request");
    return await response.json();
  } catch (error) {
    console.error("Error creating group request:", error);
    return null;
  }
}

export async function deleteGroupRequest(groupId, studentId = 1) {
  try {
    const response = await fetch(
      `${API_BASE}/group-requests/${groupId}/${studentId}`,
      {
        method: "DELETE",
      },
    );
    if (!response.ok) throw new Error("Failed to delete group request");
    return await response.json();
  } catch (error) {
    console.error("Error deleting group request:", error);
    return null;
  }
}

export async function fetchAssessments() {
  try {
    const response = await fetch(`${API_BASE}/assessments`);
    if (!response.ok) throw new Error("Failed to fetch assessments");
    return await response.json();
  } catch (error) {
    console.error("Error fetching assessments:", error);
    return [];
  }
}

export async function fetchUnitAssessments(unitCode) {
  try {
    const response = await fetch(`${API_BASE}/units/${unitCode}/assessments`);
    if (!response.ok) throw new Error("Failed to fetch unit assessments");
    return await response.json();
  } catch (error) {
    console.error("Error fetching unit assessments:", error);
    return [];
  }
}

export async function fetchAssessmentGroups(unitCode, assessmentNum) {
  try {
    const response = await fetch(
      `${API_BASE}/units/${unitCode}/assessments/${assessmentNum}/groups`,
    );
    if (!response.ok) throw new Error("Failed to fetch assessment groups");
    return await response.json();
  } catch (error) {
    console.error("Error fetching assessment groups:", error);
    return [];
  }
}

export async function authenticateUser(username, password) {
  console.log("in authenticate");
  const response = await fetch(`${API_BASE}/auth`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    console.log(await response.json());
  }
  console.log(response);
  return await response.json();
}
