// Narrative Generation Module - Generates key nodes and life summaries
class NarrativeGenerationModule {
    constructor() {
        this.keyNodes = [];
        this.narrativeTemplates = {
            childhood: [
                "At age {age}, {name} {event}",
                "During childhood, {name} experienced {event}",
                "A pivotal moment came at age {age} when {name} {event}"
            ],
            teenage: [
                "The teenage years brought {event} for {name}",
                "At {age}, {name} faced {event}",
                "Adolescence marked a turning point: {name} {event}"
            ],
            adult: [
                "As an adult, {name} {event}",
                "At age {age}, {name} made a significant decision: {event}",
                "A major life change occurred when {name} {event}"
            ],
            elderly: [
                "In later years, {name} {event}",
                "Reflecting on life at {age}, {name} {event}",
                "The golden years brought {event} for {name}"
            ]
        };
    }

    // Generate narrative for an event
    generateNarrative(event, character, age) {
        const ageGroup = this.getAgeGroup(age);
        const templates = this.narrativeTemplates[ageGroup] || this.narrativeTemplates.adult;
        const template = templates[Math.floor(Math.random() * templates.length)];
        
        return template
            .replace('{name}', character.name)
            .replace('{age}', age)
            .replace('{event}', event);
    }

    // Identify key life nodes
    identifyKeyNodes(lifeEvents, state, attributes) {
        const nodes = [];
        
        // Education milestones
        if (state.individualState.education >= 50 && !nodes.find(n => n.type === 'education')) {
            nodes.push({
                type: 'education',
                age: this.findEventAge(lifeEvents, 'education'),
                title: 'Educational Achievement',
                description: 'Reached significant educational milestone'
            });
        }
        
        // Career milestones
        if (state.individualState.careerLevel >= 50 && !nodes.find(n => n.type === 'career')) {
            nodes.push({
                type: 'career',
                age: this.findEventAge(lifeEvents, 'career'),
                title: 'Career Breakthrough',
                description: 'Achieved significant career advancement'
            });
        }
        
        // Relationship milestones
        if (state.relationshipState.romantic.status === 'married') {
            nodes.push({
                type: 'marriage',
                age: this.findEventAge(lifeEvents, 'marriage'),
                title: 'Marriage',
                description: 'Got married and started a family'
            });
        }
        
        if (state.relationshipState.children.count > 0) {
            nodes.push({
                type: 'parenthood',
                age: this.findEventAge(lifeEvents, 'child'),
                title: 'Parenthood',
                description: `Became a parent of ${state.relationshipState.children.count} child(ren)`
            });
        }
        
        // Wealth milestones
        if (attributes.wealth >= 80) {
            nodes.push({
                type: 'wealth',
                age: this.findEventAge(lifeEvents, 'wealth'),
                title: 'Financial Success',
                description: 'Achieved significant financial success'
            });
        }
        
        // Social milestones
        if (state.socialState.influence >= 70) {
            nodes.push({
                type: 'influence',
                age: this.findEventAge(lifeEvents, 'influence'),
                title: 'Social Influence',
                description: 'Gained significant social influence'
            });
        }
        
        return nodes;
    }

    // Find event age from life events
    findEventAge(lifeEvents, type) {
        const event = lifeEvents.find(e => e.type === type || e.event.toLowerCase().includes(type));
        return event ? event.age : 0;
    }

    // Get age group
    getAgeGroup(age) {
        if (age <= 12) return 'childhood';
        if (age <= 18) return 'teenage';
        if (age <= 50) return 'adult';
        return 'elderly';
    }

    // Generate comprehensive life summary
    generateLifeSummary(character, state, attributes, lifeEvents, worldEra) {
        const summary = {
            overview: this.generateOverview(character, attributes),
            keyMoments: this.identifyKeyNodes(lifeEvents, state, attributes),
            achievements: this.generateAchievements(state, attributes),
            relationships: this.generateRelationshipSummary(state),
            legacy: this.generateLegacy(character, state, attributes),
            eraContext: this.generateEraContext(worldEra)
        };
        
        return summary;
    }

    // Generate life overview
    generateOverview(character, attributes) {
        const finalWealth = Math.round(attributes.wealth);
        const finalIntelligence = Math.round(attributes.intelligence);
        const finalCharm = Math.round(attributes.charm);
        const finalHealth = Math.round(attributes.health);
        
        let evaluation = '';
        if (finalWealth > 80 && finalIntelligence > 70) {
            evaluation = 'lived a successful and wealthy life';
        } else if (finalHealth > 80 && finalCharm > 70) {
            evaluation = 'lived a healthy and happy life';
        } else if (finalIntelligence > 80) {
            evaluation = 'lived a wise and intellectual life';
        } else if (attributes.age > 80) {
            evaluation = 'lived a long and fulfilling life';
        } else {
            evaluation = 'lived an ordinary but authentic life';
        }
        
        return {
            name: character.name,
            mbti: character.mbti.type,
            age: attributes.age,
            evaluation: evaluation,
            attributes: {
                intelligence: finalIntelligence,
                charm: finalCharm,
                health: finalHealth,
                wealth: finalWealth
            }
        };
    }

    // Generate achievements
    generateAchievements(state, attributes) {
        const achievements = [];
        
        if (state.individualState.education >= 80) {
            achievements.push('Highly educated');
        }
        
        if (state.individualState.careerLevel >= 70) {
            achievements.push('Successful career');
        }
        
        if (attributes.wealth >= 80) {
            achievements.push('Financial success');
        }
        
        if (state.socialState.influence >= 70) {
            achievements.push('Social influence');
        }
        
        if (state.relationshipState.children.count > 0) {
            achievements.push(`Parent of ${state.relationshipState.children.count} child(ren)`);
        }
        
        if (state.individualState.lifeSatisfaction >= 80) {
            achievements.push('High life satisfaction');
        }
        
        return achievements;
    }

    // Generate relationship summary
    generateRelationshipSummary(state) {
        return {
            family: {
                status: state.relationshipState.family.parents,
                relationship: Math.round(state.relationshipState.family.relationship)
            },
            romantic: {
                status: state.relationshipState.romantic.status,
                quality: Math.round(state.relationshipState.romantic.quality)
            },
            friendships: {
                count: Math.round(state.relationshipState.friendships.count),
                quality: Math.round(state.relationshipState.friendships.quality)
            },
            children: {
                count: state.relationshipState.children.count,
                relationship: Math.round(state.relationshipState.children.relationship)
            }
        };
    }

    // Generate legacy
    generateLegacy(character, state, attributes) {
        const legacy = [];
        
        if (state.relationshipState.children.count > 0) {
            legacy.push(`Left behind ${state.relationshipState.children.count} child(ren) as a legacy`);
        }
        
        if (state.socialState.influence >= 60) {
            legacy.push('Made a significant impact on society');
        }
        
        if (state.individualState.careerLevel >= 70) {
            legacy.push('Built a successful career that inspired others');
        }
        
        if (attributes.wealth >= 70) {
            legacy.push('Accumulated wealth that benefited family and community');
        }
        
        if (legacy.length === 0) {
            legacy.push('Lived a life that touched those around them');
        }
        
        return legacy;
    }

    // Generate era context
    generateEraContext(worldEra) {
        const eraInfo = worldEra.getEraDescription();
        return {
            primaryEra: eraInfo.name,
            description: eraInfo.description,
            worldState: eraInfo.state
        };
    }
}

